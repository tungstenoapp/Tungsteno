from sympy import parse_expr

from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Plus(Module):

    def run(self, *arguments):
        return sum(arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test numerical sum
        test.assertEqual(evaluation.evaluate_code('1+1+2')[0], 4)

        # Test symbolic sum.
        test.assertEqual(evaluation.evaluate_code(
            'x+x+x')[0], parse_expr("3*x")
        )

        # Test symbolic sum.
        test.assertEqual(evaluation.evaluate_code(
            '1/2+1/3')[0], parse_expr("5/6")
        )
