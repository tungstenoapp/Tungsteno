from tsteno.notebook import Notebook as NotebookObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Notebook(Module):

    def run(self, cells):
        return NotebookObj(cells)

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        pass
