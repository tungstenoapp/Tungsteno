import unittest
from tsteno.kernel.kernel import Kernel

from sympy import parse_expr

kernel = Kernel()
evaluation = kernel.get_kext('eval')


class TestTokenizer(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(evaluation.evaluate_code('1+1+1')[0], 3)
        self.assertEqual(evaluation.evaluate_code('1+x')[0], parse_expr("x+1"))
        self.assertEqual(evaluation.evaluate_code(
            '1+x+x')[0], parse_expr("2*x+1")
        )


if __name__ == '__main__':
    unittest.main()
