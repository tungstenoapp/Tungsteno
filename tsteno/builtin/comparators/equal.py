"""
This file contains class definition for creating a equal comparator.
"""
import operator as op

from tsteno.atoms.comparator import Comparator
from tsteno.atoms.module import Module, ModuleArg


class Equal(Module):
    """
    Represent an equal operator.
    ## Examples
    Test equality.

    **Input:**
    ```
    # Equal[x+1, 1+x]
    x + 1 == 1 + x
    ```

    **Output:**
    ```
    True
    ```
    ---
    Represent an equation

    **Input:**
    ```
    # Solve[Equal[x+1, 0, x]
    Solve[x+1==0, x]
    ```

    **Output:**
    ```
    {{x->-1}}
    ```
    """

    def run(self, left, right):
        """
        Represent an equal operator.
        Parameters:
            - **left**: Left element to be compared.
            - **right**: Right element to be compared.
        """
        return Comparator(left, right, op.eq)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertTrue(evaluation.evaluate_code('x+1==1+x').eval())
        test.assertFalse(evaluation.evaluate_code('x+1==x').eval())

        test.assertEqual(str(evaluation.evaluate_code('1==1')), 'True')
