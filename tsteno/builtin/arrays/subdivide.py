"""
This file contains class definition for working with List.
"""
import sympy as sp
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Subdivide(Module):
    """
    **Subdivide[n]**
    Generates the list {0,1/n,2/n,…,1}.

    # Examples
    Basic list of 4 elements.

    **<u>Input:</u>**
    ```
    Subdivide[10]
    ```

    **<u>Output:</u>**
    ```
    [0, 1/10, 1/5, 3/10, 2/5, 1/2, 3/5, 7/10, 4/5, 9/10, 1]

    ---
    **Subdivide[xmax, n]**
    generates the list of values obtained by subdividing the interval 0 to xmax into n equal parts.

    # Examples
    Basic list of 4 elements.

    **<u>Input:</u>**
    ```
    Subdivide[10, 5]
    ```

    **<u>Output:</u>**
    ```
    {0, 2, 4, 6, 8, 10}

    """

    def run(self, *arguments):
        start = 0
        stop = 1
        num = 0

        if len(arguments) == 1:
            num = arguments[0]
        elif len(arguments) == 2:
            stop = arguments[0]
            num = arguments[1]
        elif len(arguments) == 3:
            start = arguments[0]
            stop = arguments[1]
            num = arguments[2]

        if isinstance(start, int) and isinstance(stop, int):
            start = sp.core.Integer(start)
            stop = sp.core.Integer(stop)

        return list(self.subdivide(start, stop, num))

    def subdivide(self, start, stop, num=50, endpoint=True):
        num = int(num) + 1
        start = start
        stop = stop

        if num == 1:
            yield stop
            return
        if endpoint:
            step = (stop - start) / (num - 1)
        else:
            step = (stop - start) / num

        for i in range(num):
            yield start + step * i

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass
