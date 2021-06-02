"""
Represent basic Tungsteno Language modules representation
"""

from .atoms import Atoms

ARG_FLAG_OPTIONAL = 1 << 1
""" Specify if given argument is optional """

ARG_FLAG_ALL_NEXT = 1 << 2
""" Specify if you want to receive the rest of argument as list """

ARG_FLAG_NO_AUTO_EVAL = 1 << 3
""" Specify if you want to read argument as executable lambda function """

ARG_FLAG_SPECIAL_CONTEXT = 1 << 4
""" Special argument used to receive execution context """

ARG_FLAG_RETURN_VAR_NAME = 1 << 5
""" Special argument that return var name """

ARG_FLAG_ALLOW_APPLY = 1 << 6
""" If variable is a list, apply to all elements individually """


class ModuleArg:
    """
    Represent module argument type configuration
    """
    __slots__ = ['__flag']

    def __init__(self, flag=0):
        """
        Parameters:
            - **flag** - Represent argument type flag. (Default user given value)
        """
        self.__flag = flag

    def get_flag(self):
        """
        Return:
            - Return module arg flag.
        """
        return self.__flag

    def __repr__(self):
        return 'ModuleArg: {}'.format(self.__flag)


class UserArgMultiValue:
    __slots__ = ['__multival']

    def __init__(self, multival=[]):
        """
        Parameters:
            - **multival**
        """
        self.__multival = multival

    def get_multival(self):
        return self.__multival


class Module(Atoms):
    """
    Super class that represent basic Tungsteno Language modules.
    """

    def eval(self, arguments, context):
        """
        Eval function with given arguments.

        Parameters:
            - **arguments** - Represent function arguments.
            - **context** - Represent local context to execute function.

        Return:
            - Function execution result.
        """
        properties = {}
        fargs = self.parse_arguments(arguments, context, properties)

        if 'MultiValueFun' in properties:
            k = 0
            for arg in fargs:
                if isinstance(arg, UserArgMultiValue):
                    return self.run_multivalue(k, fargs)
        return self.run(*fargs)

    def parse_arguments(self, arguments, context, properties=None):
        """
        Parse given arguments in given context.

        Parameters:
            - **arguments** - Represent function arguments.
            - **context** - Represent local context to execute function.

        Return:
            - **list** - Python friendly function arguments.
        """
        fargs = []
        argssize = len(arguments)
        module_args = self.get_arguments()
        users_args_counter = 0

        for i in range(0, len(module_args)):
            module_arg = module_args[i]

            if module_arg.get_flag() == ARG_FLAG_SPECIAL_CONTEXT:
                fargs.append(context)
                continue

            if module_arg.get_flag() & ARG_FLAG_OPTIONAL != 0 and \
                    i >= argssize:
                break

            if module_arg.get_flag() & ARG_FLAG_ALL_NEXT != 0:
                return fargs + list(map(lambda arg: self.parse_argument(
                    module_arg, arg, context), arguments[users_args_counter:]
                ))

            if i >= argssize:
                raise Exception(
                    "Expected but {} arguments but {} given".format(
                        len(module_args), argssize
                    ))
            user_arg = arguments[users_args_counter]
            users_args_counter = users_args_counter + 1

            farg = self.parse_argument(module_arg, user_arg, context)
            if isinstance(farg, UserArgMultiValue) and properties is not None:
                properties['MultiValueFun'] = True
            if farg is not None:
                fargs.append(farg)

        return fargs

    def parse_argument(self, module_arg, user_arg, context):
        """
        Parse one argument by child class configuration, and user given argument.

        Parameters:
            - **module_arg** - Argument child class configuration
            - **user_arg** - Argument from user input.
            - **context** - Represent local context to execute function.

        Return:
            - Return one pythonic parsed argument.
        """

        eval = self.get_kernel().get_kext('eval')

        if module_arg.get_flag() & ARG_FLAG_RETURN_VAR_NAME != 0:
            context.set_no_var_mode(1)

        if module_arg.get_flag() & ARG_FLAG_NO_AUTO_EVAL == 0:
            if isinstance(user_arg, list):
                def eval_fn(args, context):
                    return list(map(lambda arg: eval.evaluate_node(
                        arg, context
                    ), args))[-1]
            else:
                eval_fn = eval.evaluate_node
        else:
            if isinstance(user_arg, list):
                def eval_fn(args, context):
                    return lambda ctx=context: list(
                        map(lambda arg: eval.evaluate_node(arg, ctx), args))[-1]
            else:
                def eval_fn(args, context):
                    return lambda ctx=context: eval.evaluate_node(
                        args, ctx
                    )

        result = eval_fn(user_arg, context)

        if module_arg.get_flag() & ARG_FLAG_RETURN_VAR_NAME != 0:
            context.set_no_var_mode(0)

        if module_arg.get_flag() & ARG_FLAG_ALLOW_APPLY != 0 and isinstance(result, list):
            return UserArgMultiValue(result)

        return result

    def configuration_list2dict(self, list_of_properties):
        """
        Helper function that converts list of rules to dictionary.
        Parameters:
            - **list_of_properties** -  List of rules.
        Return:
            - **dict** - Result of convert list of properties to dict.
        """
        prop_dict = {}

        for prop in list_of_properties:
            prop_key = list(prop.rules_dict.keys())[0]
            prop_dict[prop_key] = prop[prop_key]

        return prop_dict

    def run_multivalue(self, idxmultivalue, fargs):
        results = []
        multivalue_array = fargs[idxmultivalue].get_multival()

        for val in multivalue_array:
            fargs[idxmultivalue] = val
            results.append(self.run(*fargs))

        return results

    def run(self, **arguments):
        """
        Run module itself. Should be implemented by child class.
        Parameters:
            - **arguments** - List of arguments.
        """
        raise Exception("eval function should be defined")

    def run_parallel(self, **arguments):
        """
        Should be implemented by child class, by default call to run
        Parameters:
            - **arguments** - List of arguments.
        """
        return self.run(arguments)

    def get_arguments(self):
        """
        Get module arguments configuration. Should be implemented by child
        class.
        Parameters:
            - **arguments** - List of arguments.
        """
        raise Exception("get_arguments function should be defined")

    def run_test(self, test):
        """
        Configure module tests. Should be implemented by child
        """
        raise Exception(
            "Run test function is undefined on `{}`".format(
                self.__class__.__name__
            )
        )

    def __repr__(self, arguments=None):
        return self.__class__.__name__
