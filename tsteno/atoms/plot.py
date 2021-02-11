class Plot:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z
