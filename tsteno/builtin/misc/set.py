from tsteno.kernel.kexts.evaluation import EVAL_FLAG_RETURN_VAR_NAME
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT


class Set(Module):

    def run(self, var, value, context):
        evaluation = self.get_kernel().get_kext('eval')
        evaluation.set_global_user_variable(str(var), value)

        return True

    def get_arguments(self):
        return [
            ModuleArg(EVAL_FLAG_RETURN_VAR_NAME), ModuleArg(
            ), ModuleArg(ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Set[a, 2]; Return[a+1]')[1], 3)
