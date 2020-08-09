from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_SPECIAL_CONTEXT
from tsteno.atoms.module import ARG_FLAG_RETURN_VAR_NAME
from tsteno.builtin.misc.custom_module import UserDefinedModule


class Set(Module):

    def define_one(self, evaluation, variable, value, context):
        if isinstance(value, Module):
            variable_name = variable.head
            value.set_param_mapping(variable.childrens)
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

            variable_name = variable.get_value()

        define_var_fn(variable_name, value)

    def run(self, all_variables, all_values, context):
        evaluation = self.get_kernel().get_kext('eval')

        if not isinstance(all_variables, list):
            all_variables = [all_variables]

        if not isinstance(all_values, list):
            all_values = [all_values]

        definers = zip(all_variables, all_values)

        for definer in definers:
            self.define_one(evaluation, definer[0], definer[1], context)

        return all_values

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_RETURN_VAR_NAME),
            ModuleArg(),
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Set[a, 2]; Return[a+1]'), 3)

        test.assertEqual(evaluation.evaluate_code(
            'Set[TFD[x_], Module[{x0=x, c}, c=10; x0 + c]]; TFD[2]'), 12)

        test.assertEqual(evaluation.evaluate_code(
            '{a, b, c} = {1, 2, 3}; b'), 2)
