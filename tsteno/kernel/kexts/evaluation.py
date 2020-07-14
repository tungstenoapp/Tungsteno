import os
from .log import LogLevel
from .kext_base import KextBase
from importlib.machinery import SourceFileLoader

PROTECTED_NAMES_BUILTIN = ['builtin_base.py', '__init__.py']

class Evaluation(KextBase):
    __slots__ = ['ker_definitions']

    def __init__(self, kernel):
        super().__init__(kernel)
        log_kext = self.get_kernel().get_kext('log')
        log_kext.write('Starting definitions for eval kext...', LogLevel.DEBUG)
        self.ker_definitions = {}

        if self.get_kernel().parent is None:
            self.__bootstrap(log_kext)

        log_kext.write('Definitions for eval kext loaded succesfully!', LogLevel.DEBUG)

    def __search_builtin(self, path=os.path.join(
        os.path.dirname(__file__), '..', '..', 'builtin')
    ):
        modules = []
        list_dir = os.listdir(path)
        for file in list_dir:
            fullpath = os.path.join(path, file)

            module_name = fullpath.split(os.path.sep)[-1]
            module_name = module_name[:-3]
            module_name = ''.join(
                x.capitalize() or '_' for x in module_name.split('_')
            )

            if file in PROTECTED_NAMES_BUILTIN:
                continue

            if os.path.isdir(fullpath):
                modules = modules + self.__search_builtin(fullpath)
            elif file.endswith('.py'):
                modules.append({'path': fullpath, 'module': module_name})

        return modules

    def __bootstrap(self, log_kext):
        builtin_modules = self.__search_builtin()

        log_kext.write(
            f'We have found {len(builtin_modules)} builtin modules',
            LogLevel.DEBUG
        )

        for builtin_module in builtin_modules:
            log_kext.write(
                f"Loading `{builtin_module['module']}`...",
                LogLevel.DEBUG
            )

            module = SourceFileLoader(
                builtin_module['module'], builtin_module['path']
            )
            module = module.load_module()

            definition = getattr(module, builtin_module['module'])()

            self.ker_definitions[builtin_module['module']] = definition

            log_kext.write(
                f"Loaded `{builtin_module['module']}` succesfully!",
                LogLevel.DEBUG
            )

        log_kext.write(
            f'{len(builtin_modules)} builtin modules loaded succesfully',
            LogLevel.DEBUG
        )





