from .tokenizer import NumberToken, IdentifierToken, ClosureToken, FunctionIdentifierToken, ListSeparatorToken, BinOpToken
from collections import namedtuple

OpInfo = namedtuple('OpInfo', 'prec assoc function')

OPINFO_MAP = {
    '=':    OpInfo(0, 'LEFT', 'Set'),
    '+':    OpInfo(1, 'LEFT', 'Plus'),
    '-':    OpInfo(1, 'LEFT', 'Minus'),
    '*':    OpInfo(2, 'LEFT', 'Product'),
    '/':    OpInfo(2, 'LEFT', 'Div'),
    '^':    OpInfo(3, 'RIGHT', 'Pow'),
}

class ParserOutput:

    @staticmethod
    def is_match(token):
        """ Check if given character match with token character list 

        Keyword arguments:
        character -- character to be checked
        """
        raise Exception("Method not defined")

    @staticmethod
    def parse(parser):
        """ After a match, generate a token class from the current buffer. 

        Keyword arguments:
        tokenizer -- current buffer
        """
        raise Exception("Method not defined")

class ExpressionParserOutput(ParserOutput):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    @staticmethod
    def is_match(token):
        return isinstance(token, NumberToken) or isinstance(token, IdentifierToken)

    @staticmethod
    def parse(parser, min_prec = 0):
        atom_lhs = ExpressionParserOutput.compute_atom(parser)

        while (parser.current_pos < len(parser.tokens) and 
            not isinstance(parser.curtok, ClosureToken) and
            parser.curtok != None):

            cur = parser.curtok
            op = cur.get_value()
            prec, assoc, function = OPINFO_MAP[op]

            if (cur is None or 
                not isinstance(cur, BinOpToken) or 
                prec < min_prec):
                break

            next_min_prec = prec + 1 if assoc == 'LEFT' else prec
            parser.get_next_token()
            atom_rhs = ExpressionParserOutput.parse(parser, next_min_prec)

            atom_lhs = FunctionExpressionParserOutput(function, [atom_lhs, atom_rhs])

        return atom_lhs
        
    @staticmethod
    def compute_atom(parser):
        token = parser.curtok
        parser.get_next_token()

        if token == None:
            return None

        if isinstance(token, NumberToken):
            return NumberExpressionParserOutput(token.get_value())
        elif isinstance(token, FunctionIdentifierToken):
            arguments = []

            for arg_token in token.arguments:
                if isinstance(arg_token, ListSeparatorToken):
                    continue

                arg_parser = Parser([arg_token])
                arg_parser_result = arg_parser.get_next_parser_output()

                arguments.append(arg_parser_result)

            return FunctionExpressionParserOutput(token.fname, arguments)
        elif isinstance(token, IdentifierToken):
            return ExpressionParserOutput(token.get_value())

        raise Exception("Unknown token type")    

    def __repr__(self):
        return str(self.value)

class NumberExpressionParserOutput(ExpressionParserOutput):
    pass

class FunctionExpressionParserOutput(ExpressionParserOutput):
    __slots__ = ['fname', 'arguments']

    def __init__(self, fname, arguments):
        self.fname = fname
        self.arguments = arguments
    
    def __repr__(self):
        output = self.fname + "["
        for arg in self.arguments:
            output += str(arg) + ", "
        output = output[:-2]
        output += "]"

        return output

class Parser:
    AVAILABLE_PARSER_OUT = [
        ExpressionParserOutput
    ]

    __slots__ = ['tokens', 'current_pos', 'curtok', 'toklen']

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = -1
        self.toklen = len(self.tokens)
        self.get_next_token()

    def get_next_token(self):
        self.current_pos = self.current_pos + 1
        self.curtok = self.tokens[self.current_pos] if self.toklen > self.current_pos else None
        return self.curtok

    def get_current_token(self):
        return self.curtok

    def get_next_parser_output(self):
        if self.curtok == None:
            return None

        if isinstance(self.curtok, ClosureToken):
            self.get_next_token()
            return self.get_next_parser_output()

        for parser_output in Parser.AVAILABLE_PARSER_OUT:
            if parser_output.is_match(self.curtok):
                return parser_output.parse(self)

        raise Exception("Unexpected " + str(self.curtok))

    def get_all_parser_output(self):
        parser_output = self.get_next_parser_output()
        parser_output_all = []

        while parser_output != None:
            parser_output_all.append(parser_output)
            parser_output = self.get_next_parser_output()

        return parser_output_all
