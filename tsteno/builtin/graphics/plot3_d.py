import numpy as np
from tsteno.atoms.module import Module, ModuleArg
from tsteno.atoms.module import ARG_FLAG_NO_AUTO_EVAL
from tsteno.atoms.module import ARG_FLAG_SPECIAL_CONTEXT
from tsteno.atoms.plot import Plot as Plt

PLOT_ACCURACY = 200


class Plot3D(Module):
    """
    Generates a three-dimensional plot of f as a function of x and y.
    ```
    Plot3D[f,{x,xmin,xmax},{y,ymin,ymax}]
    ```

    # Examples
    ```
    Plot3D[Sin[x + y^2], {x, -3, 3}, {y, -2, 2}]
    ```
    """

    def run(self, f, variables1, variables2, context):
        x = variables1[0]
        x0 = variables1[1]
        xmax = variables1[2]

        y = variables2[0]
        y0 = variables2[1]
        ymax = variables2[2]

        x_points = np.linspace(x0, xmax)
        y_points = np.linspace(y0, ymax)

        z_points = []

        for x0 in x_points:
            row = []
            for y0 in y_points:
                row.append(self.evaluate_f(f, x, x0, y, y0, context))
            z_points.append(row)

        return Plt(list(x_points), list(y_points), list(z_points))

    def evaluate_f(self, f, x, x0, y, y0, context):
        context.set_local_context(True)
        context.set_user_variable(str(x), x0)
        context.set_user_variable(str(y), y0)
        fvalue = f(context)
        context.set_local_context(False)

        return fvalue

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(),
            ModuleArg(),
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code(
            'Plot3D[Sin[x + y^2], {x, -3, 3}, {y, -2, 2}]')
