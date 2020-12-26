import unittest
from tsteno.language.tokenizer import Tokenizer
import tsteno.language.token_list as token_list

tokenizer = Tokenizer()


class TestTokenizer(unittest.TestCase):

    def test_parseNumber(self):
        tokens = list(tokenizer.get_tokens("12345"))

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertEqual(token.get_type(), token_list.TOKEN_NUMBER)
        self.assertEqual(token.get_value(), 12345)

    def test_parseComment(self):
        tokens = list(tokenizer.get_tokens("(*HOLA*)12345(*a*)"))

        self.assertEqual(len(tokens), 1)

        token = tokens[0]

        self.assertEqual(token.get_type(), token_list.TOKEN_NUMBER)
        self.assertEqual(token.get_value(), 12345)

    def test_parseNumberPlusNumber(self):
        tokens = list(tokenizer.get_tokens("12345+1.23"))

        self.assertEqual(len(tokens), 3)

        self.assertEqual(tokens[0].get_type(), token_list.TOKEN_NUMBER)
        self.assertEqual(tokens[0].get_value(), 12345)

        self.assertEqual(tokens[1].get_type(), token_list.TOKEN_OP)
        self.assertEqual(tokens[1].get_value(), '+')

        self.assertEqual(tokens[2].get_type(), token_list.TOKEN_NUMBER)
        self.assertEqual(tokens[2].get_value(), 1.23)

    def test_parseEqualFn(self):
        tokens = list(tokenizer.get_tokens("a[x_] = Print[x]"))

        self.assertEqual(len(tokens), 9)

        self.assertEqual(tokens[0].get_type(), token_list.TOKEN_IDENTIFIER)
        self.assertEqual(tokens[0].get_value(), 'a')

        self.assertEqual(
            tokens[1].get_type(), token_list.TOKEN_LEFTSQUARE_BRACKETS)

        self.assertEqual(tokens[2].get_type(), token_list.TOKEN_IDENTIFIER)
        self.assertEqual(tokens[2].get_value(), 'x_')

        self.assertEqual(
            tokens[3].get_type(), token_list.TOKEN_RIGHTSQUARE_BRACKETS)

        self.assertEqual(tokens[4].get_type(), token_list.TOKEN_OP)
        self.assertEqual(tokens[4].get_value(), '=')

        self.assertEqual(tokens[5].get_type(), token_list.TOKEN_IDENTIFIER)
        self.assertEqual(tokens[5].get_value(), 'Print')

        self.assertEqual(
            tokens[6].get_type(), token_list.TOKEN_LEFTSQUARE_BRACKETS)

        self.assertEqual(tokens[7].get_type(), token_list.TOKEN_IDENTIFIER)
        self.assertEqual(tokens[7].get_value(), 'x')

        self.assertEqual(
            tokens[8].get_type(), token_list.TOKEN_RIGHTSQUARE_BRACKETS)

    def test_parseString(self):
        tokens = list(tokenizer.get_tokens('"Hola mundo, \\"Como estais\\""'))

        self.assertEqual(len(tokens), 1)

        self.assertEqual(tokens[0].get_type(), token_list.TOKEN_STRING)
        self.assertEqual(tokens[0].get_value(), 'Hola mundo, "Como estais"')


if __name__ == '__main__':
    unittest.main()
