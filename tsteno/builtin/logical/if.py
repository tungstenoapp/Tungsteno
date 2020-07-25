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
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'If[1 > 2, Return[2], Return[3]]')[0], 3)

        test.assertEqual(evaluation.evaluate_code(
            'If[1 < 2, Return[2], Return[3]]')[0], 2)
