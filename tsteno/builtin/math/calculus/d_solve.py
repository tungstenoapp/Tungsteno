import sympy
from tsteno.atoms.module import ModuleArg, Module
from tsteno.atoms.module import ARG_FLAG_OPTIONAL, ARG_FLAG_ALL_NEXT
from tsteno.atoms.rule import RuleSet


class DSolve(Module):
    """
    Gives the indefinite integral.
    ```
    Integrate[f, x]
    ```
    """

    def run(self, expr, fun, variables):
        solutions = sympy.dsolve(
            expr.left - expr.right, fun.get_sympy(), dict=True)

        return RuleSet(self.get_kernel(), {
            solutions.lhs: solutions.rhs
        })

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(),
            ModuleArg(ARG_FLAG_OPTIONAL | ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        print(evaluation.evaluate_code(
            "DSolve[y'[x] + y[x] == 5 * Sin[x], y[x], x]"))
