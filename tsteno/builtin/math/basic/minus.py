from tsteno.atoms.module import ModuleArg, Module
from sympy.parsing.sympy_parser import parse_expr


class Minus(Module):

    def run(self, a, b):
        return a - b

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test numerical minus
        test.assertEqual(evaluation.evaluate_code('1-0.5'), .5)

        # Test symbolic minus.
        test.assertEqual(evaluation.evaluate_code('x-2'), parse_expr("x-2"))

        # Test symbolic minus.
        test.assertEqual(evaluation.evaluate_code(
            '2*x-x'), parse_expr("x"))
