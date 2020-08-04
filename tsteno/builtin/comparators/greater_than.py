import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class GreaterThan(Module):

    def run(self, left, right):
        return Comparator(left, right, op.gt)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('2>1').eval())
        test.assertFalse(evaluation.evaluate_code('1>2').eval())
