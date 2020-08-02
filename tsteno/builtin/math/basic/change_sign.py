from sympy import parse_expr
from tsteno.atoms.module import Module, ModuleArg


class ChangeSign(Module):

    def run(self, a):
        return -a

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test numerical pow.
        test.assertEqual(evaluation.evaluate_code('-20')[0], -20)
        test.assertEqual(str(evaluation.evaluate_code(
            '-oo')[0]), '-oo')
