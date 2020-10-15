from tsteno.notebook.box_data import BoxData as BoxDataObj
from tsteno.atoms.module import Module, ModuleArg


class BoxData(Module):

    def run(self, boxes):
        return BoxDataObj(boxes)

    def get_arguments(self):
        return [
            ModuleArg()
        ]

    def run_test(self, test):
        pass
