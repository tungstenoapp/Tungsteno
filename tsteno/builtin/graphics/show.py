from tsteno.atoms.module import Module, ModuleArg
from tsteno.atoms.plot import PlotArray

class Show(Module):
    """
    Generates a plot of f as a function of x from xmin to xmax.
    ```
    Plot[f,{x,xmin,xmax}]
    ```

    # Examples
    ```
    Plot[Sin[x], {x, 0, 6 Pi}]
    ```
    """

    def run(self, plots):
        return PlotArray(plots)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        print(evaluation.evaluate_code(
            'pl1 = Plot[Sin[xx], {xx, 0, 10}]; pl2 = Plot[Cos[yy], {yy, 0, 10}]; Show[{pl1, pl2}]'))
