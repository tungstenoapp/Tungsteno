import string
import tsteno.language.token_list as token_list


class Token:
    __slots__ = ('type', 'val', 'pos')

    def __init__(self, toktype, tokval, pos):
        self.val = tokval
        self.type = toktype
        self.pos = pos

    def get_value(self):
        return self.val

    def get_type(self):
        return self.type

    def __repr__(self):
        return "{} : {}".format(self.type, self.val)


class BaseTokenReader:
    def __init__(self):
        pass

    def match(self, character):
        raise Exception("Undefined class reference")

    def calculate(self, code, pos, max_len):
        raise Exception("Undefined class reference")


class NumberTokenReader(BaseTokenReader):
    def match(self, character):
        return character.isdigit()

    def calculate(self, code, pos, max_len):
        num_buffer = []
        num_cls = int

        while pos < max_len:
            if not code[pos].isdigit() and (
                code[pos] != '.' or
                code[pos] in num_buffer
            ):
                break

            if code[pos] == '.':
                num_cls = float

            num_buffer.append(code[pos])
            pos = pos + 1
            continue

        return Token(
            token_list.TOKEN_NUMBER, num_cls("".join(num_buffer)), pos
        ), pos


class StringTokenReader(BaseTokenReader):

    def match(self, character):
        return character == "\""

    def calculate(self, code, pos, max_len):
        characters = []

        pos = pos + 1
        while pos < max_len:
            if code[pos] == "\"" and code[pos - 1] != "\\":
                return Token(
                    token_list.TOKEN_STRING, "".join(characters), pos
                ), pos + 1
            if code[pos] == "\\":
                pos = pos + 1
                continue
            characters.append(code[pos])
            pos = pos + 1

        raise TokenError('Unknown character', code, pos, max_len)


class IdentifierTokenReader(BaseTokenReader):
    OK_CHARACTERS = ['_']

    def match(self, character):
        return character is not None and (
            character in string.ascii_letters or
            character in IdentifierTokenReader.OK_CHARACTERS
        )

    def calculate(self, code, pos, max_len):
        characters = []

        while pos < max_len and (
            self.match(code[pos]) or
            code[pos].isdigit() or
            code[pos] in ['_']
        ):
            characters.append(code[pos])
            pos = pos + 1

        return Token(
            token_list.TOKEN_IDENTIFIER, "".join(characters), pos
        ), pos


class MiscTokenReader(BaseTokenReader):
    TOKEN_REFERENCES = {
        # Operations
        '+': token_list.TOKEN_OP,
        '-': token_list.TOKEN_OP,
        '*': token_list.TOKEN_OP,
        '/': token_list.TOKEN_OP,
        '=': token_list.TOKEN_OP,
        '^': token_list.TOKEN_OP,
        '<': token_list.TOKEN_OP,
        '>': token_list.TOKEN_OP,
        '.': token_list.TOKEN_OP,
        '!': token_list.TOKEN_OP,

        # OP order
        '(': token_list.TOKEN_LEFTPAREN,
        ')': token_list.TOKEN_RIGHTPAREN,

        # Functions
        '[': token_list.TOKEN_LEFTFUNC,
        ']': token_list.TOKEN_RIGHTFUNC,
        ',': token_list.TOKEN_COMMA_SEPARATOR,

        '{': token_list.TOKEN_LEFTLIST,
        '}': token_list.TOKEN_RIGHTLIST,

        "\n": token_list.TOKEN_NEWLINE,
        ";": token_list.TOKEN_CLOSE_EXPR,
    }

    def __init__(self):
        super().__init__()
        self.character_list = MiscTokenReader.TOKEN_REFERENCES.keys()

    def match(self, character):
        return character in self.character_list

    def calculate(self, code, pos, max_len):
        return Token(
            MiscTokenReader.TOKEN_REFERENCES[code[pos]], code[pos], pos
        ), pos + 1


class TokenError(Exception):
    __slots__ = ('error_message')

    def __init__(self, msg, code, pos, max_len):
        col = 0
        lin = 0
        i = 0

        while i < pos:
            if code[i] == "\n":
                col = 0
                lin = lin + 1
            else:
                col = col + 1
            i = i + 1

        lines = code.split("\n")

        extra_information = "\n{}\n{}".format(
            lines[0], (' '*(col)) + '^'
        )

        character = code[pos] if pos < max_len else 'EOF'
        self.error_message = "{} `{}` near line {} and column {}: {}".format(
            msg, character, lin + 1, col + 1, extra_information
        )

    def __str__(self):
        return self.error_message


class Tokenizer:
    __slots__ = ('token_processors')

    def __init__(self):
        self.token_processors = [
            NumberTokenReader(), MiscTokenReader(),
            StringTokenReader(), IdentifierTokenReader()
        ]

    def get_tokens(self, code):
        pos = 0
        max_len = len(code)
        last_token = Token(token_list.TOKEN_NOTOKEN, '', pos)

        while pos < max_len:
            if code[pos] == "\n" or code[pos] == ' ':
                pos = pos + 1
                continue
            last_token, pos = self.get_next_token(code, pos, max_len)
            yield last_token

    def get_next_token(self, code, pos, max_len):
        for processor in self.token_processors:
            if processor.match(code[pos]):
                return processor.calculate(code, pos, max_len)

        raise TokenError('Unknown character', code, pos, max_len)
