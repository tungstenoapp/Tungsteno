from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Plus(Module):

    def run(self, *arguments):
        return sum(arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]
