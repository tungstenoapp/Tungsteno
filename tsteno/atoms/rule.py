"""
Represent a set of rules
"""
from .atoms import Atoms
from sympy import mathematica_code as mcode


class RuleSet(Atoms):
    """
    Represent a set of rules
    """
    __slots__ = ['__kernel', 'rules_dict']

    def __init__(self, kernel, rules_dict):
        """
        Initialize a new RuleSet from kernel and dict.
        Parameters:
            - **kernel** - Represent Tungsteno kernel.
            - **rules_dict** - Represnet a dictionary with rules definition
        """
        super().__init__(kernel)
        self.rules_dict = rules_dict

    def __getitem__(self, x):
        if not isinstance(x, str):
            x = str(x)

        return self.rules_dict[x]

    def __repr__(self):
        output = []

        for key, val in self.rules_dict.items():
            output.append(str(mcode(key)))
            output.append('->')
            output.append(str(mcode(val)))
            output.append(',')

        del output[len(output) - 1]

        return '{' + "".join(output) + '}'
