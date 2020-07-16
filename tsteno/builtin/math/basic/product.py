import operator
from functools import reduce
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Product(Module):

    def run(self, *arguments):
        return reduce(operator.mul, arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]
