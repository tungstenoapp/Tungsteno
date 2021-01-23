import numpy as np
from tsteno.atoms.module import Module, ModuleArg
from tsteno.atoms.module import ARG_FLAG_NO_AUTO_EVAL
from tsteno.atoms.module import ARG_FLAG_SPECIAL_CONTEXT
from tsteno.atoms.plot import Plot as Plt


class Plot(Module):
    def run(self, f, variables, context):
        x = variables[0]
        x0 = variables[1]
        xmax = variables[2]

        x_points = np.linspace(x0, xmax)
        y_points = np.array([self.evaluate_f(f, x, xi, context)
                             for xi in x_points])

        return Plt(list(x_points), list(y_points))

    def evaluate_f(self, f, x, x0, context):
        context.set_local_context(True)
        context.set_user_variable(str(x), x0)
        fvalue = f(context)
        context.set_local_context(False)

        return fvalue

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(),
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code(
            'Plot[Sin[xx], {xx, 0, 10}]')
