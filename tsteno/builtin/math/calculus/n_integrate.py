from sympy import integrate, parse_expr
from tsteno.atoms.module import ModuleArg, Module
from tsteno.atoms.module import ARG_FLAG_OPTIONAL, ARG_FLAG_ALL_NEXT


class NIntegrate(Module):

    def run(self, f, *variables):
        return integrate(f, *variables).evalf()

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(),
            ModuleArg(ARG_FLAG_OPTIONAL | ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'NIntegrate[x, {x, 0, 10}]')[0], 50)

        print(evaluation.evaluate_code(
            'NIntegrate[1/(1 + x^2), {x, 0, oo}]'))
