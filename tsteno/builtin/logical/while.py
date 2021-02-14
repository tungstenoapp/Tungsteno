from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_NO_AUTO_EVAL


class While(Module):
    """
    Evaluates test, then body, repetitively, until test first fails to give True.
    ```
    While[test,body]
    ```
    """

    def run(self, test, body):
        while test().eval():
            body()

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL), ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'j = 0; While[j < 10, j++]; Return[j]'), 10)

        test.assertEqual(
            evaluation.evaluate_code(
                'x0 = 2.0; x=x0; While[x > 0, x=Log[x]]; Return[x]'),
            -0.36651292058166435
        )
