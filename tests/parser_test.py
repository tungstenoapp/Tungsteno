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

    def test_parseFunction2(self):
        tokenizer = Tokenizer('Print[1 + 1]')

        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)

        parser_outputs = parser.get_all_parser_output()

        self.assertEqual(len(parser_outputs), 1)
        print_fn = parser_outputs[0]

        self.assertEqual(print_fn.fname, "Print")

        print_fn_args = print_fn.arguments
        self.assertEqual(len(print_fn_args), 1)

        plus_fn = print_fn_args[0]

        self.assertEqual(plus_fn.fname, "Plus")

        plus_fn_args = plus_fn.arguments
        self.assertEqual(len(plus_fn_args), 2)

        for arg in plus_fn_args:
            self.assertTrue(isinstance(arg, NumberExpressionParserOutput))
            self.assertEqual(arg.value, 1)

    def test_parseList(self):
        tokenizer = Tokenizer('{1, 1, 1}')

        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)

        parser_outputs = parser.get_all_parser_output()

        self.assertEqual(len(parser_outputs), 1)

        list_fn = parser_outputs[0]
        self.assertEqual(list_fn.fname, "List")

        self.assertEqual(len(list_fn.arguments), 3)

        for arg in list_fn.arguments:
            self.assertEqual(arg.value, 1)

    def test_comparator(self):
        tokenizer = Tokenizer('1 > 2')
        tokens = tokenizer.get_tokens()

        parser = Parser(tokens)
        parser_outputs = parser.get_all_parser_output()

        self.assertEqual(len(parser_outputs), 1)

        greater_than_fn = parser_outputs[0]
        self.assertEqual(greater_than_fn.fname, "GreaterThan")

        self.assertEqual(len(greater_than_fn.arguments), 2)

        k = 1
        for arg in greater_than_fn.arguments:
            self.assertEqual(arg.value, k)
            k = k + 1


if __name__ == '__main__':
    unittest.main()
