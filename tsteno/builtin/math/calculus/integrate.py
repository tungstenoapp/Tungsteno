from sympy import integrate, parse_expr
from tsteno.atoms.module import ModuleArg, Module
from tsteno.atoms.module import ARG_FLAG_OPTIONAL, ARG_FLAG_ALL_NEXT


class Integrate(Module):

    def run(self, f, *variables):
        return integrate(f, *variables)

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(),
            ModuleArg(ARG_FLAG_OPTIONAL | ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Integrate[x, x]'), parse_expr('x**2/2'))

        test.assertEqual(evaluation.evaluate_code(
            'Integrate[x, {x, 0, 1}]'), 1 / 2)

        test.assertEqual(evaluation.evaluate_code(
            'Integrate[x * y, {x, 0, 1}, {y, 0, 1}]'), 1 / 4)

        test.assertEqual(
            evaluation.evaluate_code('Integrate[1/(x^3 + 1), {x, 0, 1}]'),
            parse_expr('log(2)/3 + sqrt(3)*pi/9'))
