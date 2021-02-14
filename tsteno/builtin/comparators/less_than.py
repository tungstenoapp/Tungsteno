"""
This file contains class definition for creating a less or equal comparator.
"""
import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class LessThan(Module):
    """
    Represent an less operator.
    # Examples
    Test equality.

    **Input:**
    ```
    # Less[x+1, 1+x]
    x + 1 < 1 + x
    ```

    **Output:**
    ```
    True
    ```
    ---
    Represent an inequation

    **Input:**
    ```
    # Reduce[Less[x+1, 0, x]
    Reduce[x+1<0, x]
    ```

    **Output:**
    ```
    {{x<-1}}
    ```
    """

    def run(self, left, right):
        """
        Represent a less operator.
        Parameters:
            - **left**: Left element to be compared.
            - **right**: Right element to be compared.
        """
        return Comparator(left, right, op.lt)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('1<2').eval())
        test.assertFalse(evaluation.evaluate_code('2<1').eval())
