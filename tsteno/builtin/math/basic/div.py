from sympy import Rational
from tsteno.atoms.module import ModuleArg, Module


class Div(Module):

    def run(self, a, b):

        if isinstance(a, int) and isinstance(b, int):
            return Rational(a, b)

        return a / b

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]
