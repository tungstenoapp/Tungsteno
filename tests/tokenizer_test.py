import unittest
from tsteno.language.tokenizer import *


class TestTokenizer(unittest.TestCase):

    def test_parseNumber(self):
        tokenizer = Tokenizer("12345")
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertTrue(isinstance(token, NumberToken))
        self.assertEqual(token.value, 12345)

    def test_parseInvisibleProduct(self):
        tokenizer = Tokenizer("2 x")
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 3)

        self.assertTrue(isinstance(tokens[0], NumberToken))
        self.assertEqual(tokens[0].value, 2)

        self.assertTrue(isinstance(tokens[1], BinOpToken))
        self.assertEqual(tokens[1].value, '*')

        self.assertTrue(isinstance(tokens[2], IdentifierToken))
        self.assertEqual(tokens[2].value, 'x')

    def test_parseNumberPlusNumber(self):
        tokenizer = Tokenizer("12345+123")
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 3)

        self.assertTrue(isinstance(tokens[0], NumberToken))
        self.assertEqual(tokens[0].value, 12345)

        self.assertTrue(isinstance(tokens[1], BinOpToken))
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

    def test_parseFunction(self):
        tokenizer = Tokenizer('Test[1, 1]')

        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertEqual(token.fname, 'Test')
        self.assertEqual(len(token.arguments), 3)
        self.assertTrue(isinstance(token.arguments[0], NumberToken))
        self.assertTrue(isinstance(token.arguments[1], ListSeparatorToken))

        self.assertTrue(isinstance(token.arguments[2], NumberToken))

    def test_parseFunction2(self):
        tokenizer = Tokenizer('Print[1 + 1]')

        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertEqual(token.fname, 'Print')
        self.assertEqual(len(token.arguments), 3)
        self.assertTrue(isinstance(token.arguments[0], NumberToken))
        self.assertTrue(isinstance(token.arguments[1], BinOpToken))
        self.assertTrue(isinstance(token.arguments[2], NumberToken))

    def test_list(self):
        tokenizer = Tokenizer('{1, 2, 3, x}')
        tokens = tokenizer.get_tokens()

        self.assertTrue(len(tokens), 1)

        list_token = tokens[0]

        tokens_without_separator = []

        for token in list_token.items:
            if isinstance(token, ListSeparatorToken):
                continue
            tokens_without_separator.append(token)

        self.assertEqual(len(tokens_without_separator), 4)

        item_1 = tokens_without_separator[0]
        self.assertTrue(isinstance(item_1, NumberToken))
        self.assertEqual(item_1.get_value(), 1)

        item_2 = tokens_without_separator[1]
        self.assertTrue(isinstance(item_2, NumberToken))
        self.assertEqual(item_2.get_value(), 2)

        item_3 = tokens_without_separator[2]
        self.assertTrue(isinstance(item_3, NumberToken))
        self.assertEqual(item_3.get_value(), 3)

        item_4 = tokens_without_separator[3]
        self.assertTrue(isinstance(item_4, IdentifierToken))
        self.assertEqual(item_4.get_value(), 'x')

    def test_comparator(self):
        tokenizer = Tokenizer('1 > 2')
        tokens = tokenizer.get_tokens()

        self.assertEqual(len(tokens), 3)
        self.assertTrue(isinstance(tokens[0], NumberToken))
        self.assertTrue(isinstance(tokens[1], BinOpToken))
        self.assertTrue(isinstance(tokens[2], NumberToken))


if __name__ == '__main__':
    unittest.main()
