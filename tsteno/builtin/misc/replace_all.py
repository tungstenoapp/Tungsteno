from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALLOW_APPLY
from tsteno.atoms.rule import RuleSet


class ReplaceAll(Module):
    def run(self, expr, rules):
        for search, repl in rules.rules_dict.items():
            expr = expr.subs(search, repl)
        return expr

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALLOW_APPLY), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')
        test.assertEqual(evaluation.evaluate_code(
            '{x, x^2, x^3, x^4} /. x -> 2'), [2, 4, 8, 16])
