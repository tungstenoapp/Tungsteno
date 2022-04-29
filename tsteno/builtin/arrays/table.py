"""
This file contains class definition for working with List.
"""
import numpy as np
from sympy import sin
from sympy.abc import x
from tsteno.atoms.module import ARG_FLAG_NO_AUTO_EVAL, ARG_FLAG_SPECIAL_CONTEXT
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT
from itertools import product


class Table(Module):
    """
    Generates a list of n copies of expr.

    # Examples
    Basic list of 4 elements.

    **Input:**
    ```
    Table[i^2, {i, 10}]
    ```

    **Output:**
    ```
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    ```

    **Input:**
    ```
    Table[10 i + j, {i, 4}, {j, 3}]
    ```

    **Output:**
    ```
     [[11, 12, 13],
             [21, 22, 23],
             [31, 32, 33],
             [41, 42, 43]]
    ```
    """

    def run(self, context, fn, *var_values_sets):
        """
        gives a nested list. The list associated with i is outermost.
        Parameters:
            - **expr**: One expression
            - **indexes**: A list of indexes
        """
        var_values_sets = list(var_values_sets)

        if len(var_values_sets) == 1 and isinstance(var_values_sets[0], int):
            return self.evaluate_one(fn, var_values_sets[0])

        var_references = {}

        for var_values in var_values_sets:
            var, values = self.calculate_evaluator(var_values, context)
            var_references[str(var)] = values

        context.set_local_context(True)

        output = self.evaluate_table(context, fn, var_references)

        context.set_local_context(False)

        return output

    def evaluate_table(self, context, fn, var_references):
        output = []

        variables = var_references.keys()
        values = var_references.values()
        combinations = product(*values)

        shapes = map(len, values)

        for one_combi in combinations:
            for one_var, one_value in zip(variables, one_combi):
                context.set_user_variable(one_var, one_value)

            output.append(fn(context))

        return np.array(output).reshape(*shapes).tolist()

    def calculate_evaluator(self, var_values, context):
        evaluation = self.get_kernel().get_kext('eval')

        var = var_values[0]
        var_values = var_values[1:]
        var_values_size = len(var_values)

        if var_values_size >= 1 and var_values_size <= 3:
            return var, evaluation.run_function('Range', var_values, context)

        return var, var_values[0]

    def evaluate_one(self, fn, times):
        return [fn()] * times

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_SPECIAL_CONTEXT),
            ModuleArg(ARG_FLAG_NO_AUTO_EVAL),
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        test.assertEqual(
            evaluation.evaluate_code('Table[Sin[x], 11]'),
            [
                sin(x), sin(x), sin(x), sin(x),
                sin(x), sin(x), sin(x), sin(x),
                sin(x), sin(x), sin(x)
            ]
        )

        test.assertEqual(evaluation.evaluate_code(
            'Table[ii^2, {ii, 10}];'), [1, 4, 9, 16, 25, 36, 49, 64, 81, 100])

        test.assertEqual(evaluation.evaluate_code(
            'Table[10*ii + jj, {ii, 4}, {jj, 3}];'),
            [[11, 12, 13],
             [21, 22, 23],
             [31, 32, 33],
             [41, 42, 43]]
        )
