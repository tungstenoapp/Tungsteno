from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class List(Module):

    def run(self, *arguments):
        return list(arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass
