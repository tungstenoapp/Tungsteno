class Atoms:
    __slots__ = ['__kernel']

    def __init__(self, kernel):
        self.__kernel = kernel

    def get_kernel(self):
        return self.__kernel
