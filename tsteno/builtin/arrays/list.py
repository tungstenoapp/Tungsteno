"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class List(Module):
    """
    Represent a list of elements.

    ## Examples
    Basic list of 4 elements.

    **Input:**
    ```
    List[a, b, c, d]
    ```

    **Output:**
    ```
    {a, b, c, d}
    ```
    """

    def run(self, *arguments):
        """
        Represent a list of elements.
        Parameters:
            - ** *arguments**: List of elements.
        """
        return list(arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3};')

        test.assertEqual(
            evaluation.evaluate_code('lista_prueba'), [1, 2, 3]
        )
