import os
import sys

from sympy import Symbol
from .log import LogLevel
from .kext_base import KextBase
from tsteno.language.ast import Node
from tsteno.language.ast import IdentifierToken
from tsteno.atoms.module import Module
from tsteno.language.parser import Parser
from tsteno.language.tokenizer import Tokenizer
import tsteno.language.token_list as token_list


if sys.version_info.major < 3 and sys.version_info.major >= 2:
    import imp
elif sys.version_info.major >= 3:
    from importlib.machinery import SourceFileLoader

from sympy import oo, pi, E, I

PROTECTED_NAMES_BUILTIN = ['builtin_base.py', '__init__.py']
MODULE_DEF_REPLACEMENT = {
    'CustomModule': 'Module'
}

CONTROL_FLOW_STATUS_P_STACK = 0
CONTROL_FLOW_STATUS_R_STACK = 1


class Context:
    __slot__ = ['__control_flow__', '__is_global__',
                '__local_context__', 'user_variables', 'user_modules',
                '__last_result__', '__no_var_mode__'
                ]

    def __init__(self):
        self.__reset__()

    def set_control_flow(self, control_flow):
        self.__control_flow__ = control_flow

    def set_last_result(self, last_result):
        self.__last_result__ = last_result

    def set_no_var_mode(self, var_mode):
        self.__no_var_mode__ = var_mode

    def get_no_var_mode(self):
        return self.__no_var_mode__

    def get_control_flow(self):
        return self.__control_flow__

    def get_last_result(self):
        return self.__last_result__

    def set_local_context(self, val):
        if not val and self.__local_context__:
            self.user_modules.clear()
            self.user_variables.clear()

        self.__local_context__ = val

    def set_user_variable(self, variable, value):
        self.user_variables[variable] = value

    def set_user_module(self, module, value):
        self.user_modules[module] = value

    def get_local_context(self):
        return self.__local_context__

    def __reset__(self):
        self.__is_global__ = True
        self.__control_flow__ = CONTROL_FLOW_STATUS_P_STACK
        self.user_variables = {}
        self.__local_context__ = False
        self.user_modules = {}
        self.__last_result__ = None
        self.__no_var_mode__ = 0


class Evaluation(KextBase):

    __slots__ = [
        'builtin_variables', 'builtin_modules',
        'user_modules', 'user_variables', 'user_modules',
        'tokenizer', 'parser', 'auto_symbols'
    ]

    def __init__(self, kernel):
        super().__init__(kernel)
        log_kext = self.get_kernel().get_kext('log')
        log_kext.write('Starting definitions for eval kext...', LogLevel.DEBUG)

        self.builtin_variables = {
            'oo': oo,
            'Pi': pi,
            'E': E,
            'I': I
        }

        self.builtin_modules = {}

        self.user_modules = {}
        self.user_variables = {}

        self.auto_symbols = {}

        self.parser = Parser()
        self.tokenizer = Tokenizer()

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
        tokens = list(self.tokenizer.get_tokens(code))
        nodes = self.parser.get_nodes(tokens)
        context = Context()

        nodes = list(nodes)
        for node in nodes:
            context.set_last_result(self.evaluate_node(node, context))
            if context.get_control_flow() == CONTROL_FLOW_STATUS_R_STACK:
                return context.get_last_result()

        if tokens[-1].get_type() != token_list.TOKEN_CLOSE_EXPR:
            self.run_function('Print', [context.get_last_result()], context)
        return context.get_last_result()

    def evaluate_node(self, node, context):
        if isinstance(node, Node):
            return self.run_function(node.head, node.childrens, context)
        elif isinstance(node, IdentifierToken) and \
                context.get_no_var_mode() == 0:
            return self.get_variable_definition(node.get_value(), context)
        return node

    def get_autocompletion(self, text, state):
        if len(text) < 2:
            return None
        autocomplete_opts = list(self.user_modules.keys())
        autocomplete_opts += list(self.builtin_modules.keys())
        autocomplete_opts += list(self.user_variables.keys())
        autocomplete_opts += list(self.builtin_variables.keys())

        options = [i for i in autocomplete_opts if i.startswith(text)]

        if state < len(options):
            return options[state]
        else:
            return None

    def get_all_definitions(self):
        autocomplete_opts = list(self.user_modules.keys())
        autocomplete_opts += list(self.builtin_modules.keys())
        autocomplete_opts += list(self.user_variables.keys())
        autocomplete_opts += list(self.builtin_variables.keys())

        return autocomplete_opts

    def get_all_modules(self):
        return list(self.builtin_modules.values())

    def run_builtin_tests(self, test):
        modules = self.get_all_modules()
        for module in modules:
            module.run_test(test)

    def run_function(self, fname, arguments, context={}):
        module_definition = self.get_module_definition(
            fname, arguments, context)
        return module_definition.eval(arguments, context)

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

        if module_def in MODULE_DEF_REPLACEMENT:
            module_def = MODULE_DEF_REPLACEMENT[module_def]

        if isinstance(definition, Module):
            self.builtin_modules[module_def] = definition
        else:
            raise Exception("Unknown builtin definition, aborted")

        log_kext.write(
            "Loaded `{}` succesfully!".format(module_def),
            LogLevel.DEBUG
        )

    def get_module_definition(self, module, arguments, context):
        if context.get_local_context():
            if module in context.user_modules:
                return context.user_modules[module]

        if module in self.user_modules:
            return self.user_modules[module]

        if module not in self.builtin_modules:
            return self.builtin_modules['Unknown'].proxy(module, arguments)

        return self.builtin_modules[module]

    def set_global_user_variable(self, variable, value):
        self.user_variables[variable] = value

    def set_global_user_module(self, module, value):
        self.user_modules[module] = value

    def get_variable_definition(self, variable, context):
        if context.get_local_context():
            if variable in context.user_variables:
                return context.user_variables[variable]

        if variable in self.user_variables:
            return self.user_variables[variable]

        if variable not in self.builtin_variables:
            if variable in self.auto_symbols:
                return self.auto_symbols[variable]
            self.auto_symbols[variable] = Symbol(variable)
            return self.auto_symbols[variable]

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
