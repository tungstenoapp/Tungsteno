""" Kernel represent basic evaluation environment """
import uuid
import datetime
from .kexts.log import Log, LogLevel
from .kexts.evaluation import Evaluation

KERNEL_DEFAULT_OPTIONS = {
    'kext_extensions': {
        'numerical': {
            'precission': 10,
        },
        'log': {
            'log_level': LogLevel.NORMAL
        }
    }
}


class Kernel:
    __slots__ = [
        'start_dt', 'kid', 'parent', 'options',
        'kext_definitions', '__kext_initialized'
    ]

    def __init__(self, parent=None, options={}):
        if parent is None:
            self.options = self.__calculate_options(
                KERNEL_DEFAULT_OPTIONS, options
            )
        else:
            self.options = options

        self.kid = uuid.uuid4()
        if parent is None:
            self.kid = 'r00t-' + self.kid

        """ Represent kernel ID """

        self.start_dt = datetime.datetime.now()
        """ Represent kernel start date """

        self.parent = parent
        """ Represent kernel parent """

        self.kext_definitions = {}
        """ Represent kernel extensions """

        self.__kext_initialized = False
        self.__bootstrap()
        self.__kext_initialized = True

    def __calculate_options(self, default, differences):
        options = default
        for key, value in differences.items():
            if isinstance(value, dict):
                options[key] = self.__calculate_options(default[key], value)
            else:
                options[key] = value

        return options

    def __bootstrap(self):
        log_kext = Log(self)
        log_kext.write(
            f'Initializing new tungsteno kernel ({self.kid})',
            LogLevel.DEBUG
        )

        self.register_kext('log', Log, log_kext=log_kext)
        self.register_kext('eval', Evaluation)

        log_kext.write(
            f'Kernel ({self.kid}) loaded succesfully!',
            LogLevel.DEBUG
        )

    def create_subkernel(self):
        return Kernel(self)

    def get_kext(self, kext_name):
        if kext_name in self.kext_definitions:
            return self.kext_definitions[kext_name]
        raise Exception(f"Kext extension `{kext_name}` doesn't exists")

    def register_kext(self, kext_name, kext_definition, log_kext=None):
        if self.__kext_initialized:
            raise Exception("Kext extensions are loaded only during bootstrap")

        if log_kext is None:
            log_kext = self.get_kext('log')

        log_kext.write(f'Kext `{kext_name}` loading...', LogLevel.DEBUG)
        self.kext_definitions[kext_name] = kext_definition(self)
        log_kext.write(
            f'Kext `{kext_name}` loaded succesfully!',
            LogLevel.DEBUG
        )

    def get_option_value(self, *args):
        value = self.options
        for arg in args:
            if arg not in value:
                raise Exception("Option doesn't exists")
            value = value[arg]
        return value

    def get_kid(self):
        return self.kid

    def __repr__(self):
        return f'KID: {self.kid}, started at {self.start_dt} kext defs: ' +\
            ', '.join(self.kext_definitions)
