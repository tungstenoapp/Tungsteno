from .log import LogLevel
from .kext_base import KextBase
from .ui import BaseUserInterface


class UserInterface(KextBase):
    __slots__ = ('user_interface')

    def __init__(self, kernel):
        super().__init__(kernel)

        log_kext = self.get_kernel().get_kext('log')
        log_kext.write(
            'Starting user interface kext...', LogLevel.DEBUG)

    def load_user_interface(self, user_interface: BaseUserInterface):
        self.user_interface = user_interface(self.get_kernel())

    def get_ui(self):
        return self.user_interface
