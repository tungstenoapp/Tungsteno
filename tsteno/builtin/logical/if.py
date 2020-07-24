from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_NO_AUTO_EVAL


class If(Module):
    def run(self, condition, t, f):
        if condition:
            return t()
        else:
            return f()

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL)
        ]

    def run_test(self, test):
        pass
