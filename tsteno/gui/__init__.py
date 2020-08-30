import os
import eel

evaluation = None


@eel.expose
def tsteno_eval(code):
    eval_result = evaluation.evaluate_code(code)
    return {'processor': 'default', 'output': str(eval_result)}


def init_gui(kernel):
    global evaluation
    evaluation = kernel.get_kext('eval')
    eel.init(os.path.join(os.path.dirname(__file__), 'static'))
    eel.start('notebook.html')
