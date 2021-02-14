import sympy as sp
from tsteno.atoms.module import ModuleArg, Module


class Expand(Module):
    """
    Expands out products and positive integer powers in expr.
    ```
    Expand[expr]
    ```

    # Examples
    **Input:**
    ```
    Expand[(x + 3)*(x + 2)]
    ```
    **Output:**
    ```
    x^2 + 5*x + 6
    ```
    """

    def run(self, f):
        return sp.expand(f)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Expand[(x - 1)*(x + 1)]'), sp.parse_expr('x**2-1'))
