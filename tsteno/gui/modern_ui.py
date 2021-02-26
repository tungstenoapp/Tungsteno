import eel
import os
from tsteno.kernel.kexts.ui import BaseUserInterface


class ModernUI(BaseUserInterface):
    def handle_oncreate_cell(cell):
        pass

    def handle_onload(self):
        # Load eel functions.
        self.modern_ui_fn = {
            'create_new_cell': eel.createNewCell
        }

        # Start notebook with a new cell.
        self.create_new_cell()

    def handle_oncreate_cell(self, cell):
        self.modern_ui_fn['create_new_cell'](cell.toDict())
