from functools import reduce
import sympy as sp
from tsteno.atoms.module import ModuleArg, Module
from tsteno.atoms.module import ARG_FLAG_OPTIONAL, ARG_FLAG_ALL_NEXT


class Expand(Module):

    def run(self, f):
        return sp.expand(f)

    def get_arguments(self):
        return [
            ModuleArg(),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Expand[(x - 1)*(x + 1)]'), sp.parse_expr('x**2-1'))
