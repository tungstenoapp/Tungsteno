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

    **<u>Input:</u>**
    ```
    # Equal[x+1, 1+x]
    x + 1 == 1 + x
    ```

    **<u>Output:</u>**
    ```
    True
    ```
    ---
    Represent an equation

    **<u>Input:</u>**
    ```
    # Solve[Equal[x+1, 0, x]
    Solve[x+1==0, x]
    ```

    **<u>Output:</u>**
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
