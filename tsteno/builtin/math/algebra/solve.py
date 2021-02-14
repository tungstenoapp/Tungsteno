import operator
from sympy import solve, Symbol
from tsteno.atoms.module import ModuleArg, Module
from tsteno.atoms.rule import RuleSet


class Solve(Module):
    """
    Attempts to solve the system expr of equations or inequalities for the variables vars.
    ```
    Solve[expr,vars]
    ```
    """

    def run(self, expressions, variables):
        if not isinstance(expressions, list):
            expressions = [expressions]

        fmt_expr = []

        for expression in expressions:
            fmt_expr.append(Solve.calculate_one_expr(expression))

        solutions = solve(fmt_expr, variables, dict=True)
        solutions = list(map(lambda d: RuleSet(
            self.get_kernel(),
            {str(k): v for k, v in d.items()}
        ), solutions))

        if len(solutions) == 1:
            return solutions[0]

        return solutions

    @staticmethod
    def calculate_one_expr(expr):
        if expr.op == operator.eq:
            return expr.left - expr.right

        return expr.eval()

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test numerical minus
        sols = evaluation.evaluate_code(
            'Solve[x+1==0, x]'
        )
        test.assertEqual(sols['x'], -1)

        eq_sols = evaluation.evaluate_code(
            'Solve[{x+y==4, 2*x+y==5}, {x, y}]'
        )

        test.assertEqual(eq_sols[Symbol('x')], 1)
        test.assertEqual(eq_sols[Symbol('y')], 3)
