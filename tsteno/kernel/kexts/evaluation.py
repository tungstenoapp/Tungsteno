import os

from sympy import Symbol
from .log import LogLevel
from .kext_base import KextBase

from tsteno.atoms.module import Module
from importlib.machinery import SourceFileLoader
from tsteno.language.tokenizer import Tokenizer

from tsteno.language.parser import Parser, FunctionExpressionParserOutput
from tsteno.language.parser import StringParserOutput, ExpressionParserOutput
from tsteno.language.parser import NumberExpressionParserOutput

PROTECTED_NAMES_BUILTIN = ['builtin_base.py', '__init__.py']


class Evaluation(KextBase):

    __slots__ = [
        'builtin_variables', 'builtin_modules',
        'user_modules', 'user_variables', 'user_modules',
        'tokenizer'
    ]

    def __init__(self, kernel):
        super().__init__(kernel)
        log_kext = self.get_kernel().get_kext('log')
        log_kext.write('Starting definitions for eval kext...', LogLevel.DEBUG)

        self.builtin_variables = {}
        self.builtin_modules = {}

        self.user_modules = {}
        self.user_variables = {}

        if self.get_kernel().parent is None:
            self.__bootstrap(log_kext)

        log_kext.write(
            'Definitions for eval kext loaded succesfully!', LogLevel.DEBUG)

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

    def evaluate_code(self, code):
        tokenizer = Tokenizer(code)
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)
        parser_outputs = parser.get_all_parser_output()

        result = []
        for parser_output in parser_outputs:
            result.append(self.evaluate_parser_output(parser_output))

        return result

    def evaluate_parser_output(self, parser_output):
        if isinstance(parser_output, FunctionExpressionParserOutput):
            module_definition = self.get_module_definition(parser_output.fname)
            return module_definition.eval(parser_output.arguments)
        elif isinstance(parser_output, StringParserOutput):
            return parser_output.value
        elif isinstance(parser_output, NumberExpressionParserOutput):
            return parser_output.value
        elif isinstance(parser_output, ExpressionParserOutput):
            return self.get_variable_definition(parser_output.value)

    def __load_builtin_module(self, path, module_def, log_kext=None):
        if log_kext is None:
            log_kext = self.get_kernel().get_kext('log')

        log_kext.write(
            f"Loading `{module_def}`...",
            LogLevel.DEBUG
        )

        module = SourceFileLoader(
            module_def, path
        )
        module = module.load_module()

        definition = getattr(module, module_def)(self.get_kernel())

        if isinstance(definition, Module):
            self.builtin_modules[module_def] = definition
        else:
            raise Exception("Unknown builtin definition, aborted")

        log_kext.write(
            f"Loaded `{module_def}` succesfully!",
            LogLevel.DEBUG
        )

    def get_module_definition(self, module):
        if module in self.user_modules:
            return self.user_modules[module]

        if module not in self.builtin_modules:
            return self.builtin_modules['Unknown'].proxy(module)

        return self.builtin_modules[module]

    def get_variable_definition(self, variable):
        if variable in self.user_variables:
            return self.user_variables[variable]

        if variable not in self.builtin_variables:
            return Symbol(variable)
        return self.builtin_variables[variable]

    def __bootstrap(self, log_kext):
        builtin_modules = self.__search_builtin()

        log_kext.write(
            f'We have found {len(builtin_modules)} builtin modules',
            LogLevel.DEBUG
        )

        for builtin_module in builtin_modules:
            self.__load_builtin_module(
                builtin_module['path'],
                builtin_module['module'],
                log_kext
            )

        log_kext.write(
            f'{len(builtin_modules)} builtin modules loaded succesfully',
            LogLevel.DEBUG
        )
