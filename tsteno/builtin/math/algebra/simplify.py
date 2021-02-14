import sympy as sp
from tsteno.atoms.module import ModuleArg, Module

SIMPLIFY_FUNCTIONS = [
    sp.simplify, sp.factor
]


class Simplify(Module):
    """
    Performs a sequence of algebraic and other transformations on expr and returns the simplest form it finds.
    ```
    Simplify[expr]
    ```

    """

    def run(self, f):
        for fn in SIMPLIFY_FUNCTIONS:
            f = fn(f)

        return f

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Simplify[x^2-1]'), sp.parse_expr('(x - 1)*(x + 1)'))

        test.assertEqual(evaluation.evaluate_code(
            'Simplify[Sin[x]^2+Cos[x]^2]'), 1)
