import unittest
from tsteno.kernel.kernel import Kernel


class TestTokenizer(unittest.TestCase):
    def test_kernelInit(self):
        kernel = Kernel()
        evaluation = kernel.get_kext('eval')

        evaluation.evaluate_code('Print[x + 1.453 + 1 + 2 + x + x^3 + 5^2]')


if __name__ == '__main__':
    unittest.main()
