from .atoms import Atoms

ARG_FLAG_OPTIONAL = 1 << 1
ARG_FLAG_ALL_NEXT = 1 << 2
ARG_FLAG_NO_AUTO_EVAL = 1 << 3
ARG_FLAG_SPECIAL_CONTEXT = 1 << 4
ARG_FLAG_RETURN_VAR_NAME = 1 << 5


class ModuleArg:
    __slots__ = ['__flag']

    def __init__(self, flag=0):
        self.__flag = flag

    def get_flag(self):
        return self.__flag

    def __repr__(self):
        return 'ModuleArg: {}'.format(self.__flag)


class Module(Atoms):

    def eval(self, arguments, context):
        fargs = self.parse_arguments(arguments, context)
        return self.run(*fargs)

    def parse_arguments(self, arguments, context):
        fargs = []
        argssize = len(arguments)
        module_args = self.get_arguments()

        for i in range(0, len(module_args)):
            module_arg = module_args[i]

            if module_arg.get_flag() == ARG_FLAG_SPECIAL_CONTEXT:
                fargs.append(context)
                continue

            if module_arg.get_flag() & ARG_FLAG_OPTIONAL != 0 and \
                    i >= argssize:
                break

            if module_arg.get_flag() & ARG_FLAG_ALL_NEXT != 0:
                return fargs + list(map(lambda arg: self.parse_argument(
                    module_arg, arg, context), arguments[i:]
                ))

            if i >= argssize:
                raise Exception(
                    "Expected but {} arguments but {} given".format(
                        len(module_args), argssize
                    ))
            user_arg = arguments[i]

            farg = self.parse_argument(module_arg, user_arg, context)
            if farg is not None:
                fargs.append(farg)

        return fargs

    def parse_argument(self, module_arg, user_arg, context):
        eval = self.get_kernel().get_kext('eval')

        if module_arg.get_flag() & ARG_FLAG_RETURN_VAR_NAME != 0:
            context.set_no_var_mode(1)

        if module_arg.get_flag() & ARG_FLAG_NO_AUTO_EVAL == 0:
            if isinstance(user_arg, list):
                def eval_fn(args, context):
                    return list(map(lambda arg: eval.evaluate_node(
                        arg, context
                    ), args))[-1]
            else:
                eval_fn = eval.evaluate_node
        else:
            if isinstance(user_arg, list):
                def eval_fn(args, context):
                    return lambda ctx=context: list(
                        map(lambda arg: eval.evaluate_node(arg, ctx), args))[-1]
            else:
                def eval_fn(args, context):
                    return lambda ctx=context: eval.evaluate_node(
                        args, ctx
                    )

        result = eval_fn(user_arg, context)

        if module_arg.get_flag() & ARG_FLAG_RETURN_VAR_NAME != 0:
            context.set_no_var_mode(0)

        return result

    def configuration_list2dict(self, list_of_properties):
        prop_dict = {}

        for prop in list_of_properties:
            prop_key = list(prop.rules_dict.keys())[0]
            prop_dict[prop_key] = prop[prop_key]

        return prop_dict

    def run(self, **arguments):
        raise Exception("eval function should be defined")

    def run_parallel(self, **arguments):
        return self.run(arguments)

    def get_arguments(self):
        raise Exception("get_arguments function should be defined")

    def run_test(self, test):
        raise Exception(
            "Run test function is undefined on `{}`".format(
                self.__class__.__name__
            )
        )

    def __repr__(self, arguments=None):
        return self.__class__.__name__
