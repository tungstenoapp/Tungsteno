"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg


class MemberQ(Module):
    """
    **MemberQ[list, item]**
    Check if item is in list
    """

    def run(self, lst, item):
        return item in lst

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg()
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,2,3,4, 5, 6};')

        test.assertEqual(
            evaluation.evaluate_code('MemberQ[lista_prueba, 10]'), False
        )

        test.assertEqual(
            evaluation.evaluate_code('MemberQ[lista_prueba, 1]'), True
        )
