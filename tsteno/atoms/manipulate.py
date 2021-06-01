class Manipulate:
    __slots__ = ('context', 'expr_pointer', 'variables')

    def __init__(self, expr_pointer, variables):

        for i in range(0, len(variables)):
            variables[i][0] = str(variables[i][0])

            if len(variables[i]) != 4:
                variables[i].append(0.1)

        self.expr_pointer = expr_pointer
        self.variables = variables
