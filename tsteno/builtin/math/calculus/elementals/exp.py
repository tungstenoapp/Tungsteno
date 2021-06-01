import sympy as sp
import numpy as np
from tsteno.atoms.module import ModuleArg, Module, ARG_FLAG_ALLOW_APPLY


class Exp(Module):
    """
    Gives the exponential of z.
    ```
    Exp[z]
    ```
    """

    def run(self, x):
        if isinstance(x, float):
            return np.exp(x)

        return sp.exp(x)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALLOW_APPLY),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Exp[1]'), evaluation.evaluate_code('E'))

        test.assertEqual(evaluation.evaluate_code(
            'Exp[0]'), 1)
