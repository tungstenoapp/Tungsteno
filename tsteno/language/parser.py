from tokenizer import BinOpToken, Tokenizer, ClosureToken
from collections import namedtuple

OpInfo = namedtuple('OpInfo', 'prec assoc')

OPINFO_MAP = {
    '+':    OpInfo(1, 'LEFT'),
    '-':    OpInfo(1, 'LEFT'),
    '*':    OpInfo(2, 'LEFT'),
    '/':    OpInfo(2, 'LEFT'),
    '^':    OpInfo(3, 'RIGHT'),
}

class ParserExpression:
    def __init__(self, _type, args):
        self.type = _type
        self.args = args

    def __repr__(self):
        build_str = self.type
        build_str += "["

        for arg in self.args:
           build_str += str(arg)
           build_str += ","

        build_str = build_str[:-1]

        build_str += "]"

        return build_str
class Parser:
    __slots__ = ['tokens', 'current_pos']

    def __init__(self, tokenizer):
        self.tokens = tokenizer.get_tokens()
        self.current_pos = 0

    def compute_atom(self):
        token = self.tokens[self.current_pos]
        self.current_pos = self.current_pos + 1

        return token.get_value()

    def compute_expr(self, min_prec):
        atom_lhs = self.compute_atom()
        
        while (self.current_pos < len(self.tokens) and 
            not isinstance(self.tokens[self.current_pos], ClosureToken)):

            cur = self.tokens[self.current_pos]
            op = cur.get_value()
            prec, assoc = OPINFO_MAP[op]

            if (cur is None or 
                not isinstance(cur, BinOpToken) or 
                prec < min_prec):
                break
            
            next_min_prec = prec + 1 if assoc == 'LEFT' else prec
            self.current_pos = self.current_pos + 1
            atom_rhs = self.compute_expr(next_min_prec)
            
            atom_lhs = self.compute_op(op, atom_lhs, atom_rhs)

        return atom_lhs
    
    def compute_op(self, op, lhs, rhs):
        if op == '+':
            return ParserExpression('Plus', [lhs, rhs])
        elif op == '*':
            return ParserExpression('Product', [lhs, rhs])

