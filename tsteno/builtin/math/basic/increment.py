from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT
from tsteno.atoms.module import ARG_FLAG_RETURN_VAR_NAME
from tsteno.language.ast import IdentifierToken


class Increment(Module):

    def run(self, var, context):
        evaluation = self.get_kernel().get_kext('eval')

        if isinstance(var, IdentifierToken):
            current_value = evaluation.get_variable_definition(
                var.get_value(), context)
            evaluation.run_function(
                'Set', [var, current_value + 1], context)
            return current_value

        return var

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_RETURN_VAR_NAME), ModuleArg(
                ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        # Test increment.
        test.assertEqual(evaluation.evaluate_code(
            'imt_1=2; Increment[imt_1]; Return[imt_1]'), 3)

        # test.assertEqual(evaluation.evaluate_code(
        #    'imt2=2; imt2++'), 2)
