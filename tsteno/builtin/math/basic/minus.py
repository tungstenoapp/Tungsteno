from tsteno.atoms.module import ModuleArg, Module


class Minus(Module):

    def run(self, a, b):
        return a - b

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]
