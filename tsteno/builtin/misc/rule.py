from tsteno.atoms.module import Module, ModuleArg
from tsteno.atoms.rule import RuleSet


class Rule(Module):

    def run(self, key, value):
        return RuleSet(self.get_kernel(), {str(key): value})

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):

        evaluation = self.get_kernel().get_kext('eval')
        rule = list(evaluation.evaluate_code(
            '{x -> 1}'))[0]
        test.assertEqual(rule['x'], 1)
