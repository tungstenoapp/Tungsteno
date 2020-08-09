import numpy as np
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_OPTIONAL


class Range(Module):

    def run(self, a, b=None, di=1):
        if b is None:
            return np.arange(1, a+di, di)
        return np.arange(a, b+di, di)

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(ARG_FLAG_OPTIONAL),
            ModuleArg(ARG_FLAG_OPTIONAL)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(list(evaluation.evaluate_code(
            'Range[2, 5]')), [2, 3, 4, 5])

        test.assertEqual(list(evaluation.evaluate_code(
            'Range[5]')), [1, 2, 3, 4, 5])

        test.assertEqual(list(evaluation.evaluate_code(
            'Range[1, 5, 0.5]')), [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
