from tsteno.notebook.cell import CellGroupData as CellGroupDataObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class CellGroupData(Module):

    def run(self, cells):
        return CellGroupData(cells)

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        pass
