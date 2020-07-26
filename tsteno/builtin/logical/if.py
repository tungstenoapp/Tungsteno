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

        test.assertEqual(evaluation.evaluate_code(
            'If[1 < 2, i = 0; i = i + 1; i = i * 3.14; Return[i], Return[1]]')[0], 3.14)
