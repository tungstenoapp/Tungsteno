"""
Contains atoms super class.
"""


class Atoms:
    """
    Atoms super class used to abstract atoms.
    """

    __slots__ = ['__kernel']

    def __init__(self, kernel):
        """
        Create a new atoms instance.

        Parameters:
            - **kernel** - Represent a Tungsteno kernel instance

        """
        self.__kernel = kernel

    def get_kernel(self):
        """
        Return current configured kernel in current atom.

        Return:
            Configured kernel.
        """
        return self.__kernel
