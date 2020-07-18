from sympy import integrate
from tsteno.atoms.module import ModuleArg, Module


class Integrate(Module):

    def run(self, f, x):
        return integrate(f, x)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]
