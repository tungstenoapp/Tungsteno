
from .log import LogLevel
from .kext_base import KextBase


class Output(KextBase):
    __slots__ = ('handlers')

    def __init__(self, kernel):
        super().__init__(kernel)

        log_kext = self.get_kernel().get_kext('log')
        log_kext.write(
            'Starting output interface for eval kext...', LogLevel.DEBUG)

        self.handlers = []

    def write(self, obj):
        for handler in self.handlers:
            handler(obj)

    def register_output_handler(self, handler):
        self.handlers.append(handler)
