from tsteno.notebook import Notebook as NotebookObj
from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Notebook(Module):

    def run(self, cells, *nb_properties):
        nb_properties = self.configuration_list2dict(nb_properties)
        return NotebookObj(cells, nb_properties)

    def get_arguments(self):
        return [
            ModuleArg(), ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass
