from .atoms import Atoms

ARG_FLAG_OPTIONAL = 1 << 1
ARG_FLAG_ALL_NEXT = 1 << 2


class ModuleArg:
    __slots__ = ['__flag']

    def __init__(self, flag=0):
        self.__flag = flag

    def get_flag(self):
        return self.__flag


class Module(Atoms):

    def eval(self, arguments):
        fargs = []
        module_args = self.get_arguments()
        eval = self.get_kernel().get_kext('eval')

        for i in range(0, len(module_args)):
            module_arg = module_args[i]

            if module_arg.get_flag() & ARG_FLAG_ALL_NEXT != 0:
                fargs = fargs + \
                    list(map(eval.evaluate_parser_output, arguments[i:]))
                break

            fargs.append(eval.evaluate_parser_output(arguments[i]))

        return self.run(*fargs)

    def run(self, **arguments):
        raise Exception("eval function should be defined")

    def run_parallel(self, **arguments):
        return self.run(arguments)

    def get_arguments(self):
        raise Exception("get_arguments function should be defined")

    def __repr__(self, arguments=None):
        return self.__class__.__name__
