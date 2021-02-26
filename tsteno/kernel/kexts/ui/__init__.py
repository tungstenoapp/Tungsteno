from tsteno.kernel.kexts.ui.cell import Cell
from ..log import LogLevel


class BaseUserInterface:
    __slots__ = ('user_interface', 'properties', 'cells')

    def __init__(self, kernel):
        self.kernel = kernel
        self.cells = []

        log_kext = self.kernel.get_kext('log')
        log_kext.write(
            'Starting ' + self.__class__.__name__, LogLevel.DEBUG)

    def load(self):
        self.handle_onload()

    # Configure UI properties
    def set_properties(self, properties):
        self.properties = properties
        self.handle_on_update_properties()

    # Create new cell.
    def create_new_cell(self, content=None, status=None, properties={}):
        new_cell = Cell(len(self.cells), content, status, properties)

        self.cells.append(new_cell)

        self.handle_oncreate_cell(new_cell)

    # Called after create new cell.
    def handle_oncreate_cell(self, cell):
        pass

    # Handle when BaseUserInterface is loaded.
    def handle_onload(self):
        pass

    # Called after properties updated.
    def handle_on_update_properties(self):
        pass
