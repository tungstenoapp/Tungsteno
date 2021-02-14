import sympy as sp
import numpy as np
from tsteno.atoms.module import ModuleArg, Module


class Cos(Module):
    """
    Gives the cosine of z.
    ```
    Cos[z]
    ```
    """

    def run(self, x):
        if isinstance(x, float):
            return np.cos(x)

        return sp.cos(x)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Cos[Pi]'), -1)

        test.assertEqual(evaluation.evaluate_code(
            'Cos[2*Pi]'), 1)

        test.assertEqual(evaluation.evaluate_code(
            'Cos[Pi/2]'), 0)

        test.assertEqual(evaluation.evaluate_code(
            'Cos[1.0]^2 + Sin[1.0]^2'), 1.0)
