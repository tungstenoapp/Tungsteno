from tsteno.kernel.kexts.evaluation import EVAL_FLAG_RETURN_VAR_NAME
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT
from tsteno.builtin.misc.custom_module import UserDefinedModule


class Set(Module):

    def run(self, variable, value, context):
        evaluation = self.get_kernel().get_kext('eval')

        if isinstance(value, Module):
            variable_name = variable.fname
            value.set_param_mapping(variable.arguments)
            if context.get_local_context():
                define_var_fn = context.set_user_module
            else:
                define_var_fn = evaluation.set_global_user_module
        else:
            if context.get_local_context():
                define_var_fn = context.set_user_variable
            else:
                define_var_fn = evaluation.set_global_user_variable

            if hasattr(value, '__call__'):
                value = value()

            variable_name = variable

        define_var_fn(variable_name, value)

        return True

    def get_arguments(self):
        return [
            ModuleArg(EVAL_FLAG_RETURN_VAR_NAME),
            ModuleArg(),
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Set[a, 2]; Return[a+1]')[1], 3)

        test.assertEqual(evaluation.evaluate_code(
            'Set[TFD[x_], Module[{x0=x, c}, c=10; x0 + c]]; TFD[2]')[1], 12)
