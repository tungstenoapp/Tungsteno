from sympy.parsing.sympy_parser import parse_expr
from tsteno.atoms.module import Module, ModuleArg


class Pow(Module):

    def run(self, a, b):
        return a**b

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test symbolic pow
        test.assertEqual(evaluation.evaluate_code('x^2'), parse_expr("x**2"))

        # Test numerical pow.
        test.assertEqual(evaluation.evaluate_code(
            '2^10'), 2**10
        )
