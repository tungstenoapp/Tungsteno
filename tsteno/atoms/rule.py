from .atoms import Atoms


class RuleSet(Atoms):
    __slots__ = ['__kernel', 'rules_dict']

    def __init__(self, kernel, rules_dict):
        super().__init__(kernel)
        self.rules_dict = rules_dict

    def __getitem__(self, x):
        if not isinstance(x, str):
            x = str(x)

        return self.rules_dict[x]

    def __repr__(self):
        output = []
        for key, val in self.rules_dict.items():
            output.append(str(key))
            output.append('->')
            output.append(str(val))
            output.append(',')

        del output[len(output) - 1]

        return '{' + "".join(output) + '}'
