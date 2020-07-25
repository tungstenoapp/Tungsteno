from tsteno.kernel.kexts.evaluation import CONTROL_FLOW_STATUS_R_STACK
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT


class Return(Module):

    def run(self, result, context):
        context.set_control_flow(CONTROL_FLOW_STATUS_R_STACK)
        return result

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg(ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Return[1]; Return[2]; Print[3]')[0], 1)
