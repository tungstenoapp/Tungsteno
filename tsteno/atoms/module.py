from .atoms import Atoms


class Module(Atoms):

    def eval(self, **arguments):
        raise Exception("eval function should be defined")

    def get_arguments(self):
        raise Exception("get_arguments function should be defined")
