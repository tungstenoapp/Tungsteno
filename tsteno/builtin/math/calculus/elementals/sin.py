import sympy as sp
import numpy as np
from tsteno.atoms.module import ModuleArg, Module


class Sin(Module):
    """
    Gives the sine of z.
    ```
    Sin[z]
    ```
    """

    def run(self, x):
        if isinstance(x, float):
            return np.sin(x)

        return sp.sin(x)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Sin[Pi]'), 0)

        test.assertEqual(evaluation.evaluate_code(
            'Sin[2*Pi]'), 0)

        test.assertEqual(evaluation.evaluate_code(
            'Sin[Pi/2]'), 1)

        test.assertEqual(evaluation.evaluate_code(
            'Sin[1.0]'), 0.8414709848078965)
