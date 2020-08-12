from tsteno.notebook.cell import Cell as CellObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Cell(Module):

    def run(self, *contents):
        return CellObj(contents)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass
