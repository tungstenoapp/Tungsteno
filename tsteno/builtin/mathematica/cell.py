from tsteno.notebook.cell import Cell as CellObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT, ARG_FLAG_OPTIONAL


class Cell(Module):

    def run(self, cell_content, status=None, *cell_properties):
        cell_properties = self.configuration_list2dict(cell_properties)

        return CellObj(cell_content, status, cell_properties)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg(ARG_FLAG_OPTIONAL),
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass
