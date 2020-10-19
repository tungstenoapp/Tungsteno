"""
Contains comparator operator atom.
"""
from .atoms import Atoms
from functools import reduce


class Comparator(Atoms):
    """
    Comparator represent a binary operation that compare two values.
    """
    __slots__ = ('left', 'right', 'op')

    def __init__(self, left, right, op):
        """
        Parameters:
            ** left ** - Left value to be compared.
            ** right ** - Right value to be compared.
            ** op ** -  Operator used to compare.
        """
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        """
        Evaluate current comparator and generate an answer.

        Return:
            Return a boolean value if left & right are numeric.
            Return a symbol if left or right are symbols.
        """
        return reduce(self.op, (self.left, self.right))

    def __bool__(self):
        """
        Shortcut to eval()
        """
        return self.eval()

    def __repr__(self):
        return str(self.eval()).capitalize()
