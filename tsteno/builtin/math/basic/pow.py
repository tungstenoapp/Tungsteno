from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Pow(Module):

    def run(self, a, b):
        return a**b

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]
