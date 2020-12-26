"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class Drop(Module):
    """
    **Drop[list, item]**
    Drop item from array
    """

    def run(self, take_from, take):
        new_list = take_from[:]

        if isinstance(take, list):
            del new_list[take[0] - 1:take[1]]
        elif take < 0:
            del new_list[take:]
        else:
            del new_list[:take]

        return new_list

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3,4, 5, 6};')

        test.assertEqual(
            evaluation.evaluate_code('Drop[lista_prueba, 2]'),  [3, 4, 5, 6]
        )

        test.assertEqual(
            evaluation.evaluate_code('Drop[lista_prueba, -3]'),  [1, 2, 3]
        )

        test.assertEqual(
            evaluation.evaluate_code('Drop[lista_prueba, {2, 4}]'),  [1, 5, 6]
        )
