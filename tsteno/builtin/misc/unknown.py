from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Unknown(Module):

    def run(self, *arguments):
        return self.__repr__(arguments)

    def proxy(self, fname):
        return UnknownProxy(self.get_kernel(), fname)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass


class UnknownProxy(Unknown):
    def __init__(self, kernel, fname):
        super().__init__(kernel)
        self.fname = fname

    def __repr__(self, arguments=None):
        argument_repr = ", ".join(list(map(lambda x: str(x), arguments)))
        return "{}[{}]".format(self.fname, argument_repr)
