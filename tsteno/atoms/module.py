import numbers
from .atoms import Atoms

ARG_FLAG_OPTIONAL = 1 << 1
ARG_FLAG_ALL_NEXT = 1 << 2
ARG_FLAG_NO_AUTO_EVAL = 1 << 3
ARG_FLAG_SPECIAL_CONTEXT = 1 << 4


class ModuleArg:
    __slots__ = ['__flag']

    def __init__(self, flag=0):
        self.__flag = flag

    def get_flag(self):
        return self.__flag


class Module(Atoms):

    def eval(self, arguments, context):
        fargs = []
        module_args = self.get_arguments()
        eval = self.get_kernel().get_kext('eval')

        for i in range(0, len(module_args)):
            module_arg = module_args[i]

            if module_arg.get_flag() == ARG_FLAG_SPECIAL_CONTEXT:
                fargs.append(context)
                continue
            if isinstance(arguments[i], str) or \
                    isinstance(arguments[i], numbers.Number):
                fargs.append(arguments[i])
                continue
            if module_arg.get_flag() & ARG_FLAG_NO_AUTO_EVAL == 0:
                eval_fn = eval.evaluate_parser_output
            else:
                def eval_fn(args, context, flag):
                    return lambda: eval.evaluate_parser_output(args, context, flag=flag)

            if module_arg.get_flag() & ARG_FLAG_ALL_NEXT != 0:
                fargs = fargs + \
                    list(map(lambda x: eval_fn(x, context,
                                               flag=module_arg.get_flag()), arguments[i:]))
                break

            fargs.append(
                eval_fn(arguments[i], context, flag=module_arg.get_flag()))
        return self.run(*fargs)

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
