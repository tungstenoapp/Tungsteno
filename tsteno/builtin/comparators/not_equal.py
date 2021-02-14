"""
This file contains class definition for creating a less or equal comparator.
"""
import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class NotEqual(Module):
    """
    Represent an not equal operator.
    # Examples
    Test equality.

    **Input:**
    ```
    # NotEqual[x+1, 1+x]
    x + 1 != 1 + x
    ```

    **Output:**
    ```
    False
    ```
    """

    def run(self, left, right):
        """
        Represent a not equal operator.
        Parameters:
            - **left**: Left element to be compared.
            - **right**: Right element to be compared.
        """
        return Comparator(left, right, op.ne)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('x+1!=2+x').eval())
        test.assertFalse(evaluation.evaluate_code('x+1!=x+1').eval())
