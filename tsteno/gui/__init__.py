import os
import eel
import sympy
import traceback
import difflib
import math
import numpy
import tsteno.notebook.export

from sympy import mathematica_code as mcode
from tsteno.notebook import Notebook
from tsteno.atoms.plot import Plot, PlotArray
from tsteno.atoms.manipulate import Manipulate
from tsteno.atoms.rule import RuleSet

from tsteno.kernel.kexts.evaluation import Context
evaluation = None
output = None
eel_configuration = {}


@eel.expose
def ping():
    return 'pong'


def int2rgb(value):
    rng = numpy.random.RandomState(value)

    blue = rng.randint(0, 256)
    green = rng.randint(0, 256)
    red = rng.randint(0, 256)

    return "#%02x%02x%02x" % (red, green, blue)


@eel.expose
def evaluate_manipulate(expr_pointer, variables):
    global output

    expr, context = evaluation.get_expr_pointer(int(expr_pointer))
    for varname, varvalue in variables.items():
        evaluation.set_global_user_variable(varname, varvalue)
    eval_result = expr(context)

    for varname, varvalue in variables.items():
        evaluation.unset_global_user_variable(varname)

    return prepropcess_output(eval_result, [parse_output(eval_result)])


def prepropcess_output(eval_result, output_result):

    if isinstance(eval_result, sympy.Expr):
        return {
            'processor': 'default',
            'result': "\n".join(output_result)
        }
    elif isinstance(eval_result, Manipulate):
        return {
            'processor': 'manipulate',
            'ranges': eval_result.variables,
            'expr': eval_result.expr_pointer
        }
    elif isinstance(eval_result, Plot) or isinstance(eval_result, PlotArray):
        plot_data = []
        k = 0

        if isinstance(eval_result, PlotArray):
            for plot in eval_result.plots:
                new_plot = {}

                new_plot['x'] = plot.x
                new_plot['y'] = plot.y

                if plot.z is not None:
                    new_plot['z'] = plot.z

                new_plot['type'] = 'scatter'
                new_plot['modes'] = 'lines'
                new_plot['marker'] = {
                    'color': int2rgb(k)
                }

                plot_data.append(new_plot)
                k = k + 1
        else:
            plot_data = [{
                'x': eval_result.x,
                'y': eval_result.y,
                'type': 'scatter',
                'mode': 'lines',
                'marker': {
                        'color': int2rgb(k)
                }
            }]

            if eval_result.z is not None:
                plot_data[0]['z'] = eval_result.z
                plot_data[0]['type'] = 'surface'
                plot_data[0]['showscale'] = False

        return {
            'processor': 'plot',
            'plot_data': plot_data
        }

    return {'processor': 'default', 'result': "\n".join(output_result)}


def parse_output(obj):
    to_print = obj

    if isinstance(to_print, RuleSet):
        to_print = str(to_print)
    elif not isinstance(to_print, str) and not (
        isinstance(to_print, Plot) or
        isinstance(to_print, PlotArray) or
        isinstance(to_print, Manipulate)
    ):
        to_print = mcode(to_print)

    return to_print


@eel.expose
def evaluate(code):
    global output

    output_result = []

    def gui_printer(obj):
        if obj is None or isinstance(obj, Notebook):
            return

        output_result.append(parse_output(obj))

    output.deregister_output_handlers()
    output.register_output_handler(gui_printer)

    try:
        eval_result = evaluation.evaluate_code(code)
    except Exception as err:
        print(traceback.format_exc())
        print(err)
        return {'processor': 'error', 'error': str(err)}

    return prepropcess_output(eval_result, output_result)


@eel.expose
def read_file(input_file):
    nb_file = open(input_file, 'r')
    eval_result = evaluation.evaluate_code(nb_file.read())

    if not isinstance(eval_result, Notebook):
        raise Exception("Expected notebook")

    return eval_result.dump()


@eel.expose
def read_notebook(file_data):
    eval_result = evaluation.evaluate_code(file_data)

    if not isinstance(eval_result, Notebook):
        raise Exception("Expected notebook")

    return eval_result.dump()


@eel.expose
def suggestions(input):
    global evaluation

    options = []
    input_len = len(input)

    if input_len < 2:
        return options

    definitions = evaluation.get_all_definitions()

    for definition in definitions:
        seq = difflib.SequenceMatcher(None, input, definition)

        options.append({
            'name': definition,
            'value': definition,
            'score': seq.ratio()
        })

    options.sort(key=lambda op: op['score'], reverse=True)
    options = options[:10]

    return options


@eel.expose
def searchFunction(search):
    global evaluation

    search_results = []

    for definition in evaluation.builtin_modules.keys():
        module_def = evaluation.builtin_modules[definition]
        seq = difflib.SequenceMatcher(None, search, definition)

        description = ''

        if module_def.__doc__ is not None:
            description = module_def.__doc__.replace('    ', '')

        mult = 1
        if search in definition:
            mult = 2
        if seq.ratio() > 0:
            search_results.append({
                'functionName': definition,
                'description': description,
                'score': mult * seq.ratio()
            })

        if len(description) > 0:
            abstract = description.strip().split("\n")[0]
            seq = difflib.SequenceMatcher(None, search, abstract)
            mult = 1
            if search in abstract:
                mult = 2
            if seq.ratio() > 0:
                search_results.append({
                    'functionName': definition,
                    'description': description,
                    'score': seq.ratio() * mult
                })

    search_results.sort(key=lambda op: op['score'], reverse=True)

    return search_results[:3]


@eel.expose
def get_eel_configuration():
    global eel_configuration
    return eel_configuration


@eel.expose
def export_nb(cells):
    return tsteno.notebook.export.export_nb(cells)


@eel.expose
def getVersion():
    return tsteno.VERSION


def init_gui(kernel, input_file, launcher, http_port):
    global evaluation
    global output
    global eel_configuration

    if input_file is not None:
        eel_configuration['input_file'] = input_file

    output = kernel.get_kext('output')
    evaluation = kernel.get_kext('eval')

    eel.init(os.path.join(os.path.dirname(__file__), 'static'))

    eel_mode = 'web'

    if launcher:
        eel_mode = False

    eel.start('', mode=eel_mode, all_interfaces=False, port=int(http_port))
