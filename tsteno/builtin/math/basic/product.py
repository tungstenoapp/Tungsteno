import operator
from sympy import parse_expr
from functools import reduce
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Product(Module):

    def run(self, *arguments):
        return reduce(operator.mul, arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test numerical sum
        test.assertEqual(evaluation.evaluate_code('3*1*2')[0], 6)

        # Test symbolic sum.
        test.assertEqual(evaluation.evaluate_code(
            'x*x*x')[0], parse_expr("x**3")
        )

        # Test symbolic sum.
        test.assertEqual(evaluation.evaluate_code(
            '6/3*3/6')[0], 1
        )
