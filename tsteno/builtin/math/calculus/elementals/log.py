import sympy as sp
import numpy as np
from tsteno.atoms.module import ModuleArg, Module


class Log(Module):
    """
    Gives the natural logarithm of z (logarithm to base ).
    ```
    Log[z]
    ```
    """

    def run(self, x):
        if isinstance(x, float):
            return np.log(x)

        return sp.log(x)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Log[Exp[1]]'), evaluation.evaluate_code('1'))

        test.assertEqual(evaluation.evaluate_code(
            'Log[Exp[0]]'), 0)
