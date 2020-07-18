import unittest
from tsteno.kernel.kernel import Kernel

from sympy import parse_expr

kernel = Kernel()
evaluation = kernel.get_kext('eval')


class TestTokenizer(unittest.TestCase):
    def test_all_modules(self):
        evaluation.run_builtin_tests(self)


if __name__ == '__main__':
    unittest.main()
