import operator
from sympy import solve, Symbol
from tsteno.atoms.module import ModuleArg, Module


class Solve(Module):

    def run(self, expressions, variables):
        if not isinstance(expressions, list):
            return solve(
                Solve.calculate_one_expr(expressions),
                variables,
                dict=True
            )

        fmt_expr = []

        for expression in expressions:
            fmt_expr.append(Solve.calculate_one_expr(expression))

        return solve(fmt_expr, variables, dict=True)

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
        test.assertEqual(evaluation.evaluate_code(
            'Solve[x+1==0, x]'), [{Symbol('x'): -1}]
        )

        eq_sols = evaluation.evaluate_code(
            'Solve[{x+y==4, 2*x+y==5}, {x, y}]'
        )[0]

        test.assertEqual(eq_sols[Symbol('x')], 1)
        test.assertEqual(eq_sols[Symbol('y')], 3)
