from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_NO_AUTO_EVAL


class While(Module):
    """
    Evaluates test, then body, repetitively, until test first fails to give True.
    ```
    While[test,body]
    ```
    """

    def run(self, test, body):
        while bool(test()):
            body()

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL), ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'j = 0; While[j < 10, j++]; Return[j]'), 10)
