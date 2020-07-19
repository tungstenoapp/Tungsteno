from .atoms import Atoms
from functools import reduce


class Comparator(Atoms):
    __slots__ = ('left', 'right', 'op')

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        return reduce(self.op, (self.left, self.right))

    def __repr__(self):
        return str(self.eval()).capitalize()
