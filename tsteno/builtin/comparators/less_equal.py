"""
This file contains class definition for creating a less or equal comparator.
"""

import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class LessEqual(Module):
    """
    Represent an greater or equal operator.
    # Examples
    Test equality.

    **<u>Input:</u>**
    ```
    # LessEqual[x+1, 1+x]
    x + 1 <= 1 + x
    ```

    **<u>Output:</u>**
    ```
    True
    ```
    ---
    Represent an inequation

    **<u>Input:</u>**
    ```
    # Reduce[LessEqual[x+1, 0, x]
    Reduce[x+1<=0, x]
    ```

    **<u>Output:</u>**
    ```
    {{x<=-1}}
    ```
    """

    def run(self, left, right):
        return Comparator(left, right, op.le)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('1<=2').eval())
        test.assertFalse(evaluation.evaluate_code('2<=1').eval())
