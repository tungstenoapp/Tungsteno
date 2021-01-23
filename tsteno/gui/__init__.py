import os
import eel
import sympy
import traceback
import difflib

from sympy import mathematica_code as mcode
from tsteno.notebook import Notebook

from tsteno.atoms.plot import Plot

evaluation = None
output = None
eel_configuration = {}


@eel.expose
def evaluate(code):
    global output

    output_result = []

    def gui_printer(obj):
        if obj is None or isinstance(obj, Notebook):
            return

        to_print = obj

        if not isinstance(to_print, str) and not isinstance(to_print, Plot):
            to_print = mcode(to_print)

        output_result.append(to_print)

    output.deregister_output_handlers()
    output.register_output_handler(gui_printer)

    try:
        eval_result = evaluation.evaluate_code(code)
    except Exception as err:
        print(traceback.format_exc())
        print(err)
        return {'processor': 'error', 'error': str(err)}

    if isinstance(eval_result, sympy.Expr):
        return {
            'processor': 'default',
            'result': "\n".join(output_result)
        }
    elif isinstance(eval_result, Plot):
        plot_data = [{
            'x': eval_result.x,
            'y': eval_result.y,
            'type': 'scatter',
            'mode': 'lines',
            'marker': {
                    'color': 'red'
            }
        }]

        if eval_result.z is not None:
            plot_data[0]['z'] = eval_result.z
            plot_data[0]['type'] = 'surface'

        return {
            'processor': 'plot',
            'plot_data': plot_data
        }

    return {'processor': 'default', 'result': "\n".join(output_result)}


@eel.expose
def read_file(input_file):
    nb_file = open(input_file, 'r')
    eval_result = evaluation.evaluate_code(nb_file.read())

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
def get_eel_configuration():
    global eel_configuration
    return eel_configuration


def init_gui(kernel, input_file):
    global evaluation
    global output
    global eel_configuration

    if input_file is not None:
        eel_configuration['input_file'] = input_file

    output = kernel.get_kext('output')
    evaluation = kernel.get_kext('eval')

    eel.init(os.path.join(os.path.dirname(__file__), 'static'))
    eel.start('', mode='web', all_interfaces=False)
