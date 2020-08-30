import os
import eel
import sympy

from sympy import mathematica_code as mcode

evaluation = None


@eel.expose
def tsteno_eval(code):
    eval_result = evaluation.evaluate_code(code)

    if isinstance(eval_result, sympy.Expr):
        return {
            'processor': 'default',
            'output': '$${}$$'.format(mcode(eval_result))
        }

    return {'processor': 'default', 'output': str(eval_result)}


def init_gui(kernel):
    global evaluation
    evaluation = kernel.get_kext('eval')
    eel.init(os.path.join(os.path.dirname(__file__), 'static'))
    eel.start('notebook.html')
