from sympy.core.function import Derivative, Function
from sympy.ntheory.primetest import _test
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
        evaluation = self.get_kernel().get_kext('eval')

        t = evaluation.evaluate_code(
            "chachi'[x]")

        test.assertIsInstance(t, Derivative)


class UnknownProxy(Unknown):
    def __init__(self, kernel, fname, arguments):
        super().__init__(kernel)
        self.head = fname
        self.childrens = arguments

    def __repr__(self):
        argument_repr = ", ".join(list(map(lambda x: str(x), self.childrens)))
        return "{}[{}]".format(self.head, argument_repr)

    def get_sympy(self):
        args = []

        for child in self.childrens:
            args.append(child.get_sympy())

        return Function(self.head)(*args)

    def __radd__(self, other):
        return self.get_sympy() + other

    def __rmul__(self, other):
        return self.get_sympy() * other

    def __rsub__(self, other):
        return self.get_sympy() - other

    def __rdiv__(self, other):
        return self.get_sympy() / other
