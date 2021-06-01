import sympy as sp
import numpy as np
from tsteno.atoms.module import ModuleArg, Module, ARG_FLAG_ALLOW_APPLY


class Tan(Module):
    """
    Gives the tangent of z.
    ```
    Tan[z]
    ```
    """

    def run(self, x):
        if isinstance(x, float):
            return np.tan(x)

        return sp.tan(x)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALLOW_APPLY),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')