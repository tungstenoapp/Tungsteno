from tsteno.notebook.cell import CellGroupData as CellGroupDataObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT, ARG_FLAG_OPTIONAL


class CellGroupData(Module):

    def run(self, cells, status='Open'):
        return CellGroupDataObj(cells, status)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg(ARG_FLAG_OPTIONAL)
        ]

    def run_test(self, test):
        pass
