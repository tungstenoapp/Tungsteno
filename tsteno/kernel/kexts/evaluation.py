import os
import sys

from sympy import Symbol
from .log import LogLevel
from .kext_base import KextBase

from tsteno.atoms.module import Module

if sys.version_info.major < 3 and sys.version_info.major >= 2:
    import imp
elif sys.version_info.major >= 3:
    from importlib.machinery import SourceFileLoader

from tsteno.language.tokenizer import Tokenizer

from tsteno.language.parser import Parser, FunctionExpressionParserOutput
from tsteno.language.parser import StringParserOutput, ExpressionParserOutput
from tsteno.language.parser import NumberExpressionParserOutput

PROTECTED_NAMES_BUILTIN = ['builtin_base.py', '__init__.py']

CONTROL_FLOW_STATUS_P_STACK = 0
CONTROL_FLOW_STATUS_R_STACK = 1


class Context:
    __slot__ = ['__control_flow__', '__is_global__']

    def __init__(self):
        self.__reset__()

    def set_control_flow(self, control_flow):
        self.__control_flow__ = control_flow

    def get_control_flow(self):
        return self.__control_flow__

    def __reset__(self):
        self.__is_global__ = True
        self.__control_flow__ = CONTROL_FLOW_STATUS_P_STACK


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
        context = Context()

        for parser_output in parser_outputs:
            result.append(self.evaluate_parser_output(parser_output, context))
            if context.get_control_flow() == CONTROL_FLOW_STATUS_R_STACK:
                return result

        return result

    def get_all_modules(self):
        return list(self.builtin_modules.values()) +\
            list(self.builtin_variables.values())

    def run_builtin_tests(self, test):
        modules = self.get_all_modules()
        for module in modules:
            module.run_test(test)

    def evaluate_parser_output(self, parser_output, context):
        if isinstance(parser_output, FunctionExpressionParserOutput):
            module_definition = self.get_module_definition(
                parser_output.fname, context)
            return module_definition.eval(parser_output.arguments, context)
        elif isinstance(parser_output, StringParserOutput):
            return parser_output.value
        elif isinstance(parser_output, NumberExpressionParserOutput):
            return parser_output.value
        elif isinstance(parser_output, ExpressionParserOutput):
            return self.get_variable_definition(parser_output.value, context)

    def __load_builtin_module(self, path, module_def, log_kext=None):
        if log_kext is None:
            log_kext = self.get_kernel().get_kext('log')

        log_kext.write(
            "Loading `{}`...".format(module_def),
            LogLevel.DEBUG
        )

        if sys.version_info.major < 3 and sys.version_info.major >= 2:
            module = imp.load_source(module_def, path)
        elif sys.version_info.major >= 3:
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
            "Loaded `{}` succesfully!".format(module_def),
            LogLevel.DEBUG
        )

    def get_module_definition(self, module, context):
        if module in self.user_modules:
            return self.user_modules[module]

        if module not in self.builtin_modules:
            return self.builtin_modules['Unknown'].proxy(module)

        return self.builtin_modules[module]

    def set_global_user_variable(self, variable, value):
        self.user_variables[variable] = value

    def get_variable_definition(self, variable, context):
        if variable in self.user_variables:
            return self.user_variables[variable]

        if variable not in self.builtin_variables:
            return Symbol(variable)

        return self.builtin_variables[variable]

    def __bootstrap(self, log_kext):
        builtin_modules = self.__search_builtin()

        log_kext.write(
            'We have found {} builtin modules'.format(len(builtin_modules)),
            LogLevel.DEBUG
        )

        for builtin_module in builtin_modules:
            self.__load_builtin_module(
                builtin_module['path'],
                builtin_module['module'],
                log_kext
            )

        log_kext.write(
            '{} builtin modules loaded succesfully'.format(
                len(builtin_modules)
            ),
            LogLevel.DEBUG
        )
