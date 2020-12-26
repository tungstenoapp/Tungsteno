"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class Length(Module):
    """
    **Length[list]**
    Return list size
    """

    def run(self, lst):
        return len(lst)

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3,4, 5, 6};')

        test.assertEqual(
            evaluation.evaluate_code('Length[lista_prueba]'), 6
        )
