import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class NotEqual(Module):

    def run(self, left, right):
        return Comparator(left, right, op.ne)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('x+1!=2+x')[0].eval())
        test.assertFalse(evaluation.evaluate_code('x+1!=x+1')[0].eval())
