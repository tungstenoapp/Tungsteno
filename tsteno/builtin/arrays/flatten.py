"""
This file contains class definition for working with List.
"""
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_OPTIONAL


class Flatten(Module):
    """
    **Flatten[list, lvl]**
    flattens out nested lists.
    """

    def run(self, lst, lvl=None):
        return list(self.flatten(lst, 0, lvl))

    def flatten(self, lst, current_lvl=0, lvl=None):
        for i in lst:
            if isinstance(i, (list, tuple)) and (
                    lvl is None or current_lvl < lvl):
                for j in self.flatten(i, current_lvl + 1, lvl):
                    yield j
            else:
                yield i

    def get_arguments(self):
        return [
            ModuleArg(),
            ModuleArg(ARG_FLAG_OPTIONAL)
        ]

    def run_test(self, test):
        evaluation = self.get_kernel().get_kext('eval')

        evaluation.evaluate_code('lista_prueba={1,{{2,3,4}}, 5, 6};')

        test.assertEqual(
            evaluation.evaluate_code('Flatten[lista_prueba]'), [
                1, 2, 3, 4, 5, 6]
        )

        test.assertEqual(evaluation.evaluate_code(
            'Flatten[lista_prueba, 1]'), [1, [2, 3, 4], 5, 6])
