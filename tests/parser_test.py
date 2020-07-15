import unittest
from tsteno.language.parser import *
from tsteno.language.tokenizer import *


class TestTokenizer(unittest.TestCase):
    def test_parseNumber(self):
        tokenizer = Tokenizer("12345")
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)

        parser_output = parser.get_all_parser_output()

        self.assertEqual(len(parser_output), 1)
        one_parser_output = parser_output[0]

        self.assertEqual(one_parser_output.__class__,
                         NumberExpressionParserOutput)
        self.assertEqual(one_parser_output.value, 12345)

    def test_opOrder(self):
        tokenizer = Tokenizer("1+2*3")
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)

        parser_output = parser.get_all_parser_output()

        self.assertEqual(len(parser_output), 1)

        one_parser_output = parser_output[0]

        self.assertTrue(isinstance(one_parser_output,
                                   FunctionExpressionParserOutput))
        self.assertEqual(one_parser_output.fname, "Plus")

        arguments = one_parser_output.arguments
        self.assertEqual(len(arguments), 2)
        self.assertTrue(isinstance(arguments[0], NumberExpressionParserOutput))
        self.assertEqual(arguments[0].value, 1)

        product_fn = arguments[1]

        self.assertTrue(isinstance(product_fn, FunctionExpressionParserOutput))
        self.assertEqual(product_fn.fname, "Product")

        product_args = product_fn.arguments

        self.assertEqual(len(product_args), 2)
        self.assertTrue(isinstance(
            product_args[0], NumberExpressionParserOutput))
        self.assertEqual(product_args[0].value, 2)

        self.assertTrue(isinstance(
            product_args[1], NumberExpressionParserOutput))
        self.assertEqual(product_args[1].value, 3)


if __name__ == '__main__':
    unittest.main()
