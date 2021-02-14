from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_NO_AUTO_EVAL


class For(Module):
    """
    Executes start, then repeatedly evaluates body and incr until test fails to give True.
    ```
    For[start,test,incr,body]
    ```

    # Examples
    **Input:**
    ```
    For[i = 0, i < 4, i++, Print[i]]
    ```

    **Output:**
    ```
    1
    2
    3
    4
    ```
    """

    def run(self, initial, condition, final, f):
        initial()

        while bool(condition()):
            f()
            final()

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL), ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL), ModuleArg(ARG_FLAG_NO_AUTO_EVAL)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(evaluation.evaluate_code(
            'j = 0; For[i=0, i < 10, Increment[i], j = i]; Return[j]'), 9)
