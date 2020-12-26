"""
This file contains class definition for accessing list elements
"""
import sympy
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Part(Module):
    """
    Gives the i^(th) part of expr.

    ## Examples
    Basic list of 4 elements.

    **<u>Input:</u>**
    ```
    list1 = List[a, b, c, d];
    Part[list1, 1]
    ```

    **<u>Output:</u>**
    ```
    a
    ```
    """

    def run(self, expr, *indexes):
        """
        Gives the i^(th) part of expr.
        Parameters:
            - **expr**: One expression
            - **indexes**: A list of indexes
        """
        indexes = list(indexes)

        output = self.get_element(expr, indexes[0] - 1)

        for index in indexes[1:]:
            output = self.get_element(output, index - 1)

        return output

    def get_element(self, expr, index):
        if isinstance(expr, list):
            return expr[index]
        elif isinstance(expr, sympy.Expr):
            return expr.args[index]

        raise Exception("Unable to access {} part from {}".format(index, expr))

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('part_list_test={1,2,g};')

        test.assertEqual(
            evaluation.evaluate_code('Part[{1, 10, 3, 4}, 2]'), 10
        )

        test.assertEqual(
            evaluation.evaluate_code('Part[{ {1, 2, 3, 4} }, 1]'), [1, 2, 3, 4]
        )

        test.assertEqual(
            evaluation.evaluate_code('{ {1, 2, 3, 4} }[[1]]'), [1, 2, 3, 4]
        )

        test.assertEqual(
            evaluation.evaluate_code('Part[Sin[x] + x^2+5+x, 1]'), 5
        )

        test.assertEqual(
            evaluation.evaluate_code(
                'part_list_test[[3]]'), sympy.parse_expr('g')
        )
