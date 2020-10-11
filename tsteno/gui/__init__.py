import os
import eel
import sympy
import traceback

from sympy import mathematica_code as mcode

evaluation = None


@eel.expose
def tsteno_eval(code):
    try:
        eval_result = evaluation.evaluate_code(code)
    except Exception as err:
        print(traceback.format_exc())
        print(err)
        return {'processor': 'error',  'error': str(err)}

    if isinstance(eval_result, sympy.Expr):
        return {
            'processor': 'default',
            'output': mcode(eval_result)
        }

    print(eval_result)

    return {'processor': 'default', 'output': str(eval_result)}


@eel.expose
def suggestions(input):
    global evaluation

    options = []
    input_len = len(input)

    if input_len < 2:
        return options

    definitions = evaluation.get_all_definitions()

    for definition in definitions:
        definition_len = len(definition)

        if definition.startswith(input) and definition_len - input_len > 0:
            options.append({
                'caption': definition,
                'append': definition[input_len+1:],
                'distance': definition_len - input_len
            })

    options.sort(key=lambda op: op['distance'])
    options = options[:3]

    return options


def init_gui(kernel):
    global evaluation
    evaluation = kernel.get_kext('eval')
    eel.init(os.path.join(os.path.dirname(__file__), 'static'))
    eel.start('notebook.html', mode='web', all_interfaces=False)
