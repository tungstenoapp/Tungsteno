import operator
from sympy import nsolve, Symbol
from tsteno.atoms.module import ModuleArg, Module
from random import randint
from sympy.plotting import plot


class NSolve(Module):

    def run(self, expressions, variables):
        if not isinstance(expressions, list):
            fmt_expr = NSolve.calculate_one_expr(expressions)
            return nsolve(
                fmt_expr,
                variables,
                0,
                dict=True
            )

        fmt_expr = []

        for expression in expressions:
            fmt_expr.append(NSolve.calculate_one_expr(expression))

        return nsolve(
            fmt_expr,
            variables,
            [0]*len(variables),
            dict=True,
        )

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
            'NSolve[x+1==0, x]'), [{Symbol('x'): -1}]
        )

        eq_sols = evaluation.evaluate_code(
            'NSolve[{x+y==4, 2*x+y==5}, {x, y}]'
        )[0]

        test.assertEqual(eq_sols[Symbol('x')], 1)
        test.assertEqual(eq_sols[Symbol('y')], 3)
