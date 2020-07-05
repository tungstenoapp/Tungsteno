import unittest
from tsteno.language.tokenizer import Tokenizer, NumberToken, OpToken, StringToken


class TestTokenizer(unittest.TestCase):

    def test_number2str(self):
        tokenizer = Tokenizer("12345")
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertTrue(isinstance(token, NumberToken))
        self.assertEqual(token.value, 12345)

    def test_parseNumberPlusNumber(self):
        tokenizer = Tokenizer("12345+123")
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 3)

        self.assertTrue(isinstance(tokens[0], NumberToken))
        self.assertEqual(tokens[0].value, 12345)

        self.assertTrue(isinstance(tokens[1], OpToken))
        self.assertEqual(tokens[1].value, '+')

        self.assertTrue(isinstance(tokens[2], NumberToken))
        self.assertEqual(tokens[2].value, 123)

    def test_parseString(self):
        tokenizer = Tokenizer('"Hola mundo, \\"Como estais\\""')
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertTrue(isinstance(token, StringToken))
        self.assertEqual(token.value, 'Hola mundo, "Como estais"')


if __name__ == '__main__':
    unittest.main()
