import sympy
from tsteno.kernel.kexts.evaluation import EVAL_FLAG_RETURN_VAR_NAME
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT


class Increment(Module):

    def run(self, var, context):
        evaluation = self.get_kernel().get_kext('eval')

        if isinstance(var, str):
            current_value = evaluation.get_variable_definition(var, context)
            evaluation.run_builtin_function(
                'Set', [var, current_value + 1], context)
        return var

    def get_arguments(self):
        return [
            ModuleArg(EVAL_FLAG_RETURN_VAR_NAME), ModuleArg(
                ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test increment.
        test.assertEqual(evaluation.evaluate_code(
            'imt_1=2; Increment[imt_1]; Return[imt_1]')[2], 3)
