import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class Equal(Module):

    def run(self, left, right):
        return Comparator(left, right, op.eq)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('x+1==1+x')[0].eval())
        test.assertFalse(evaluation.evaluate_code('x+1==x')[0].eval())

        test.assertEqual(str(evaluation.evaluate_code('1==1')[0]), 'True')
