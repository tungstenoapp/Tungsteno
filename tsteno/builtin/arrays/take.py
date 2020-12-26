"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class Take(Module):
    """
    **Take[list, take]**
    Return the first item of list

    """

    def run(self, take_from, take):
        if isinstance(take, list):
            return take_from[take[0] - 1:take[1]]
        if take < 0:
            return take_from[take:]
        return take_from[:take]

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3,4, 5, 6};')

        test.assertEqual(
            evaluation.evaluate_code('Take[lista_prueba, 2]'), [1, 2]
        )

        test.assertEqual(
            evaluation.evaluate_code('Take[lista_prueba, -2]'), [5, 6]
        )

        test.assertEqual(
            evaluation.evaluate_code(
                'Take[lista_prueba, {2, 4}]'), [2, 3, 4]
        )
