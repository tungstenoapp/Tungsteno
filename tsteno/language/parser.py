import numbers
from collections import namedtuple
import tsteno.language.token_list as token_list
from tsteno.language.ast import Node, IdentifierToken


class BaseParser:
    def read(self, tokens, toklen, pos, parser):
        raise Exception("Undefined `read` function")


class BasicAtomParser(BaseParser):
    def read(self, tokens, toklen, pos, parser):
        return tokens[pos].get_value(), pos + 1


class UnaryOpParser(BaseParser):
    def read(self, tokens, toklen, pos, parser):
        token = tokens[pos]

        if token.get_value() == '-':
            atom, pos = parser.compute_atom(tokens, toklen, pos + 1)

            return Node('ChangeSign', atom), pos
        elif token.get_value() == '+':
            if (pos + 1 < toklen and
                    token.get_type() == token_list.TOKEN_OP and
                    token.get_value() == '+'):
                atom, pos = parser.compute_atom(tokens, toklen, pos + 2)
                return Node('PreIncrement', atom), pos
            atom, pos = parser.compute_atom(tokens, toklen, pos + 1)
            return atom, pos

        raise Exception()


class IdentifierTokenParser(BaseParser):

    def parse_function(self, itok, tokens, toklen, pos, parser, deriv_times):
        arg = []
        arguments = []
        while pos < toklen:
            ntok = tokens[pos]

            if ntok.get_type() == token_list.TOKEN_COMMA_SEPARATOR:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                arg = []
                pos = pos + 1
                continue
            elif ntok.get_type() == token_list.TOKEN_RIGHTSQUARE_BRACKETS:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                pos = pos + 1
                break

            expr, pos = parser.compute_expr(tokens, toklen, pos)
            arg.append(expr)

        deriv_0 = Node(itok.get_value(), *arguments)

        for i in range(0, deriv_times):
            deriv_0 = Node('D', deriv_0)

        return deriv_0, pos

    def parse_access_list(self, itok, tokens, toklen, pos, parser):
        arg = []
        expr, _ = parser.compute_expr([itok], 1, 0)

        arguments = [expr]
        while pos < toklen:
            ntok = tokens[pos]

            if ntok.get_type() == token_list.TOKEN_COMMA_SEPARATOR:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                arg = []
                pos = pos + 1
                continue
            elif ntok.get_type() == token_list.TOKEN_RIGHTSQUARE_BRACKETS:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                pos = pos + 1
                break

            expr, pos = parser.compute_expr(tokens, toklen, pos)
            arg.append(expr)

        return Node('Part', *arguments), pos

    def read(self, tokens, toklen, pos, parser):
        itok = tokens[pos]

        deriv_times = 0
        if pos + 1 < toklen:
            ntok = tokens[pos + 1]
            while ntok.get_value() == "'":
                deriv_times += 1
                pos = pos + 1
                if len(tokens) > pos + 1:
                    ntok = tokens[pos + 1]
                    continue
                break

            if deriv_times > 0 or ntok.get_type() == token_list.TOKEN_LEFTSQUARE_BRACKETS:
                pos = pos + 2
                if toklen > pos and tokens[pos].get_type() == token_list.TOKEN_LEFTSQUARE_BRACKETS:
                    pos = pos + 1
                    return self.parse_access_list(itok, tokens, toklen, pos, parser)

                return self.parse_function(itok, tokens, toklen, pos, parser, deriv_times)

        return IdentifierToken(itok.get_value()), pos + 1


class ListTokenParser(BaseParser):
    def read(self, tokens, toklen, pos, parser):
        if pos < toklen:
            pos = pos + 1
            arguments = []

            while pos < toklen:
                ntok = tokens[pos]

                if ntok.get_type() == token_list.TOKEN_COMMA_SEPARATOR:
                    pos = pos + 1
                    continue
                elif ntok.get_type() == token_list.TOKEN_RIGHTLIST:
                    pos = pos + 1
                    break
                expr, pos = parser.compute_expr(tokens, toklen, pos)
                arguments.append(expr)

            return Node('List', *arguments), pos

        raise Exception()


class ParensParser(BaseParser):
    def read(self, tokens, toklen, pos, parser):
        expr, pos = parser.compute_expr(tokens, toklen, pos + 1)

        if tokens[pos].get_type() != token_list.TOKEN_RIGHTPAREN:
            raise Exception(
                "Syntax error unexpected #{} ({}) at {}".format(
                    tokens[pos].get_type(), tokens[pos].get_value(),
                    tokens[pos].pos + 1)
            )

        return expr, pos + 1


OpInfo = namedtuple('OpInfo', 'prec assoc function')

BIN_OPINFO_MAP = {
    '/.': OpInfo(-1, 'LEFT', 'ReplaceAll'),

    '->': OpInfo(0, 'LEFT', 'Rule'),
    '=': OpInfo(0, 'LEFT', 'Set'),
    ':=': OpInfo(0, 'LEFT', 'Set'),
    '<': OpInfo(0, 'LEFT', 'LessThan'),
    '<=': OpInfo(0, 'LEFT', 'LessEqual'),
    '>': OpInfo(0, 'LEFT', 'GreaterThan'),
    '>=': OpInfo(0, 'LEFT', 'GreaterEqual'),
    '==': OpInfo(0, 'LEFT', 'Equal'),
    '!=': OpInfo(0, 'LEFT', 'NotEqual'),
    '*^': OpInfo(0, 'LEFT', 'ScientificForm'),

    '+': OpInfo(1, 'LEFT', 'Plus'),
    '-': OpInfo(1, 'LEFT', 'Minus'),

    '*': OpInfo(2, 'LEFT', 'Product'),
    '/': OpInfo(2, 'LEFT', 'Div'),

    '^': OpInfo(3, 'RIGHT', 'Pow'),

}

UNARY_OPINFO_MAP = {
    '++': OpInfo(None, None, 'Increment'),
    '--': OpInfo(None, None, 'Decrement'),
    "'": OpInfo(None, None, 'D'),
}

CLOSURE_TOKENS = [
    token_list.TOKEN_CLOSE_EXPR, token_list.TOKEN_NEWLINE,
    token_list.TOKEN_COMMA_SEPARATOR, token_list.TOKEN_RIGHTSQUARE_BRACKETS,
    token_list.TOKEN_RIGHTLIST, token_list.TOKEN_RIGHTPAREN
]


class Parser:
    __slots__ = ('parser_processors', 'binary_ops')

    def __init__(self):
        basic_atom_parser = BasicAtomParser()

        self.parser_processors = {
            token_list.TOKEN_NUMBER: basic_atom_parser,
            token_list.TOKEN_STRING: basic_atom_parser,
            token_list.TOKEN_OP: UnaryOpParser(),
            token_list.TOKEN_LEFTPAREN: ParensParser(),
            token_list.TOKEN_IDENTIFIER: IdentifierTokenParser(),
            token_list.TOKEN_LEFTLIST: ListTokenParser(),
        }

    def compute_op(self, token, pos, toklen, tokens, minprec, atom_lhs):
        op = token.get_value()

        if pos + 1 < toklen and \
                tokens[pos + 1].get_type() == token_list.TOKEN_OP:
            double_op = "".join([op, tokens[pos + 1].get_value()])
            if double_op in BIN_OPINFO_MAP:
                op = double_op

        prec, assoc, node = BIN_OPINFO_MAP[op]
        if prec < minprec:
            return atom_lhs, False, pos

        next_min_prec = prec + 1 if assoc == 'LEFT' else prec

        pos = pos + len(op)

        atom_rhs, pos = self.compute_expr(
            tokens, toklen, pos, next_min_prec
        )

        atom_lhs = self.compute_binop(node, atom_lhs, atom_rhs)

        return atom_lhs, atom_rhs, pos

    def compute_number(self, tokens, toklen, pos, atom_lhs):
        prec, assoc, node = BIN_OPINFO_MAP['*']

        next_min_prec = prec + 1 if assoc == 'LEFT' else prec

        atom_rhs, pos = self.compute_expr(
            tokens, toklen, pos, next_min_prec
        )

        atom_lhs = self.compute_binop(node, atom_lhs, atom_rhs)
        return atom_lhs, atom_rhs, pos

    def compute_expr(self, tokens, toklen, pos, minprec=-1):
        atom_lhs, pos = self.compute_atom(tokens, toklen, pos)

        while pos < toklen and (
            tokens[pos].get_type() not in CLOSURE_TOKENS
        ):
            token = tokens[pos]
            next_token = None
            if pos + 1 < toklen:
                next_token = tokens[pos + 1]

            if token.get_type() == token_list.TOKEN_OP and \
                    next_token is not None and next_token.get_type() == token.get_type():
                double_op = token.get_value() + next_token.get_value()
                if double_op in UNARY_OPINFO_MAP:
                    prec, assoc, node = UNARY_OPINFO_MAP[double_op]
                    pos = pos + 2

                    atom_lhs = self.compute_unary(node, atom_lhs)
                    continue

            if token.get_type() == token_list.TOKEN_OP:
                if token.get_value() in UNARY_OPINFO_MAP:
                    prec, assoc, node = UNARY_OPINFO_MAP[token.get_value()]
                    pos = pos + 1

                    atom_lhs = self.compute_unary(node, atom_lhs)
                else:
                    atom_lhs, atom_rhs, pos = self.compute_op(
                        token, pos, toklen, tokens, minprec, atom_lhs
                    )

                    if not atom_rhs:
                        break
            elif isinstance(atom_lhs, numbers.Number):
                atom_lhs, atom_rhs, pos = self.compute_number(
                    tokens, toklen, pos, atom_lhs)
            elif token.get_type() == token_list.TOKEN_LEFTSQUARE_BRACKETS and\
                    pos + 1 < toklen and \
                    tokens[pos + 1].get_type() == token_list.TOKEN_LEFTSQUARE_BRACKETS:

                pos = pos + 2
                atom_lhs, pos = self.compute_access_list(
                    atom_lhs, tokens, toklen, pos
                )
            else:
                # nothing to do here, continue please
                break

        return atom_lhs, pos

    def compute_access_list(self, atom_lhs, tokens, toklen, pos):
        arg = []
        arguments = [atom_lhs]

        while pos < toklen:
            ntok = tokens[pos]

            if ntok.get_type() == token_list.TOKEN_COMMA_SEPARATOR:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                arg = []
                pos = pos + 1
                continue
            elif ntok.get_type() == token_list.TOKEN_RIGHTSQUARE_BRACKETS:
                arguments.append(arg[0] if len(arg) == 1 else arg)
                pos = pos + 1
                break

            expr, pos = self.compute_expr(tokens, toklen, pos)
            arg.append(expr)

        return Node('Part', *arguments), pos

    def compute_binop(self, node, lhs, rhs):
        return Node(node, lhs, rhs)

    def compute_unary(self, node, lhs):
        return Node(node, lhs)

    def compute_atom(self, tokens, toklen, pos):
        while tokens[pos].get_type() in CLOSURE_TOKENS:
            pos = pos + 1
            if pos >= toklen:
                return None, pos

        token = tokens[pos]

        if token.get_type() not in self.parser_processors:
            raise Exception(
                "Syntax error unexpected #{} ({}) at {}".format(
                    token.get_type(), token.get_value(), token.pos + 1)
            )

        return self.parser_processors[token.get_type()].read(
            tokens, toklen, pos, self
        )

    def get_nodes(self, tokens):
        pos = 0
        toklen = len(tokens)
        last_node = None

        while pos < toklen:
            last_node, pos = self.compute_expr(tokens, toklen, pos)
            if last_node is not None:
                yield last_node
