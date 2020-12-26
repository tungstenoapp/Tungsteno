"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class Append(Module):
    """
    **Append[list, item]**
    Add item to array
    """

    def run(self, take_from, item):
        new_list = take_from[:]

        new_list.append(item)

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
            evaluation.evaluate_code('Append[lista_prueba, 2]'), [
                1, 2, 3, 4, 5, 6, 2]
        )
