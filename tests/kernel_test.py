import unittest
from tsteno.kernel.kernel import Kernel


class TestTokenizer(unittest.TestCase):
    def test_kernelInit(self):
        kernel = Kernel()
        evaluation = kernel.get_kext('eval')

        evaluation.evaluate_code('Print[Integrate[1/2, x]]')


if __name__ == '__main__':
    unittest.main()
