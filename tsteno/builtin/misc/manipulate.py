from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT, ARG_FLAG_NO_AUTO_EVAL, ARG_FLAG_SPECIAL_CONTEXT

from tsteno.atoms.manipulate import Manipulate as Mpl

class Manipulate(Module):

    def run(self, context, expr, *variables):
        evaluation = self.get_kernel().get_kext('eval')

        expr_pointer = evaluation.generate_expr_pointer(expr, context)

        return Mpl(expr_pointer, variables)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT),
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')
