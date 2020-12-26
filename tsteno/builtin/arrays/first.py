"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class First(Module):
    """
    **First[list]**
    Return the first item of list

    """

    def run(self, list):
        return list[0]

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3};')

        test.assertEqual(
            evaluation.evaluate_code('First[lista_prueba]'), 1
        )
