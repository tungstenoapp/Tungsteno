from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_NO_AUTO_EVAL


class UserDefinedModule(Module):
    __slots__ = ('local_variables', 'function', 'variable_mapping', 'argsize')

    def __init__(self, kernel, local_variables, function):
        super().__init__(kernel)

        self.local_variables = local_variables
        self.function = function

    def set_param_mapping(self, arguments):
        self.variable_mapping = []
        for arg in arguments:
            self.variable_mapping.append(str(arg)[0:-1])
        self.argsize = len(self.variable_mapping)

    def eval(self, arguments, context):
        context.set_local_context(True)
        fargs = self.parse_arguments(arguments, context)

        for i in range(0, len(self.variable_mapping)):
            context.set_user_variable(self.variable_mapping[i], fargs[i])

        self.local_variables()
        execution_result = self.function()
        context.set_local_context(False)

        return execution_result

    def get_arguments(self):
        return [ModuleArg()]*self.argsize


class CustomModule(Module):

    def run(self, local_variables, function):
        return UserDefinedModule(self.get_kernel(), local_variables, function)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL), ModuleArg(ARG_FLAG_NO_AUTO_EVAL)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'Set[TFD2[x_], Module[{x0=x, c}, c=10; x0 + c]]; TFD2[2]')[1], 12)
