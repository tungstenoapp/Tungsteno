from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Unknown(Module):

    def run(self, *arguments):
        return self

    def proxy(self, fname, arguments):
        return UnknownProxy(self.get_kernel(), fname, arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass


class UnknownProxy(Unknown):
    def __init__(self, kernel, fname, arguments):
        super().__init__(kernel)
        self.head = fname
        self.childrens = arguments

    def __repr__(self):
        argument_repr = ", ".join(list(map(lambda x: str(x), self.childrens)))
        return "{}[{}]".format(self.head, argument_repr)
