"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class List(Module):
    """
    Represent a list of elements.

    ## Examples
    Basic list of 4 elements.

    **<u>Input:</u>**
    ```
    List[a, b, c, d]
    ```

    **<u>Output:</u>**
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
        pass
