""" Tokenizer generates tokens from input strings """
import string


class Token:
    """ Represent the most abstract type of token """
    __slots__ = ['value']

    def __init__(self, val):
        """
        Create a new token from given value

        Arguments:
            **val**: Set token value

        """

        self.value = val

    def get_value(self):
        """ Check if given character match with token character list

        Return:
            Token value
        """
        return self.value

    @staticmethod
    def is_match(character):
        """ Check if given character match with token character list

        Arguments:
            **character**: Character to be checked.

        Return:
            True if match, false if not.
        """
        raise Exception("Method not defined")

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(Token)* Token related to current tokenizer buffer.
        """
        raise Exception("Method not defined")

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.value)


class NumberToken(Token):
    """ Represent numeric tokens """
    @staticmethod
    def is_match(character):
        return character is not None and \
            (character.isdigit() or character == '.')

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(NumberToken)* Token related to current tokenizer buffer.
        """
        characters = [tokenizer.get_current_character()]

        while NumberToken.is_match(tokenizer.next_character()):
            characters.append(tokenizer.get_current_character())

        num_str = "".join(characters)

        if "." in characters:
            return NumberToken(float(num_str))

        return NumberToken(int(num_str))


class BinOpToken(Token):
    """ Represent binary operation tokens """

    BINARY_OP_CHARACTERS = ['+', '-', '*', '/', '^', '=', '<', '>']
    """
    Set of different binary operation characters.
    """

    COMPARATORS = ['<', '=', '>']

    @staticmethod
    def is_match(character):
        return character in BinOpToken.BINARY_OP_CHARACTERS

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(BinOpToken)* Token related to current tokenizer buffer.
        """
        op = tokenizer.get_current_character()

        next_chr = tokenizer.next_character()

        if op == '-' and next_chr == '>':
            tokenizer.next_character()
            return BinOpToken("->")
        elif op in BinOpToken.COMPARATORS and next_chr == '=':
            tokenizer.next_character()
            return BinOpToken(op + next_chr)
        elif op == '.':
            if next_chr != '/':
                raise IllegalCharacter(tokenizer)
            return BinOpToken("./")

        return BinOpToken(op)


class ListSeparatorToken(Token):
    """ Represent list separator token """
    SEPARATORS = [',']

    @staticmethod
    def is_match(character):
        return character in ListSeparatorToken.SEPARATORS

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(ListSeparatorToken)* Token related to current tokenizer buffer.
        """
        op = tokenizer.get_current_character()

        tokenizer.next_character()

        return ListSeparatorToken(op)


class ClosureToken(Token):
    """ Represent end of line or expression """

    CLOSURE_CHARACTERS = ["\n", ";"]

    @staticmethod
    def is_match(character):
        return character in ClosureToken.CLOSURE_CHARACTERS

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(ClosureToken)* Token related to current tokenizer buffer.
        """
        op = tokenizer.get_current_character()
        tokenizer.next_character()

        return ClosureToken(op)


class StringToken(Token):
    """ Represent strings """
    @staticmethod
    def is_match(character):
        return character == "\""

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(StringToken)* Token related to current tokenizer buffer.
        """
        characters = []
        finished_string = False

        while tokenizer.next_character() is not None:
            if tokenizer.get_current_character() == "\"" and \
                    (len(characters) == 0 or characters[-1] != "\\"):

                tokenizer.next_character()
                finished_string = True
                break

            if tokenizer.get_current_character() == "\"":
                characters[-1] = tokenizer.get_current_character()
            else:
                characters.append(tokenizer.get_current_character())

        if not finished_string:
            raise IllegalCharacter(tokenizer)

        return StringToken("".join(characters))


class IdentifierToken(Token):
    """ Represent variables or functions """
    @staticmethod
    def is_match(character):
        return character is not None and character in string.ascii_letters

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(IdentifierToken|FunctionIdentifierToken)* Token related to
            current tokenizer buffer.
        """
        chars = [tokenizer.get_current_character()]

        while IdentifierToken.is_match(tokenizer.next_character()) or (
                tokenizer.get_current_character() is not None and (
                    tokenizer.get_current_character().isdigit() or
                    tokenizer.get_current_character() in ['_']
                )
        ):
            chars.append(tokenizer.get_current_character())

        if FunctionIdentifierToken.is_match(tokenizer.get_current_character()):
            return FunctionIdentifierToken.parse(tokenizer, "".join(chars))

        return IdentifierToken("".join(chars))


class FunctionIdentifierToken(IdentifierToken):
    """ Represent functions """

    __slots__ = ['fname', 'arguments']

    def __init__(self, fname, arguments):
        """
        Arguments:
            **fname**: Function name\n
            **arguments**: Arguments of function
        """
        self.fname = fname
        """ Function name """
        self.arguments = arguments
        """ Function arguments """

    @staticmethod
    def is_match(character):
        return character is not None and character == '['

    @staticmethod
    def parse(tokenizer, fname):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(FunctionIdentifierToken)* Token related to
            current tokenizer buffer.
        """
        open_status = 1
        curr_character = tokenizer.next_character()

        function_arg_characters = []

        while open_status != 0 and curr_character is not None:
            if curr_character == '[':
                open_status = open_status + 1
            elif curr_character == ']':
                open_status = open_status - 1
            function_arg_characters.append(curr_character)
            curr_character = tokenizer.next_character()

        if curr_character is None and open_status != 0:
            raise IllegalCharacter(tokenizer)

        function_arg_characters = function_arg_characters[:-1]
        function_arg_code = "".join(function_arg_characters)

        args_tokenizer = Tokenizer(function_arg_code)
        try:
            tokens = args_tokenizer.get_tokens()
        except:
            raise IllegalCharacter(tokenizer)

        return FunctionIdentifierToken(fname, tokens)

    def __repr__(self):
        return '{}: {} ({})'.format(
            self.__class__.__name__,
            self.fname,
            self.arguments
        )


class ListToken(Token):
    """ Represent lists """

    __slots__ = ['items']

    def __init__(self, items):
        """
        Arguments:
            **items**: Elements\n
        """
        self.items = items
        """ Represent list items  """

    @staticmethod
    def is_match(character):
        return character is not None and character == '{'

    @staticmethod
    def parse(tokenizer):
        """ After a match, generate a token class from the current buffer.

        Arguments:
            **tokenizer**: current buffer

        Return:
            *(ListToken)* Token related to
            current tokenizer buffer.
        """
        open_status = 1
        curr_character = tokenizer.next_character()

        function_arg_characters = []

        while open_status != 0 and curr_character is not None:
            if curr_character == '{':
                open_status = open_status + 1
            elif curr_character == '}':
                open_status = open_status - 1
            function_arg_characters.append(curr_character)
            curr_character = tokenizer.next_character()

        if curr_character is None and open_status != 0:
            raise IllegalCharacter(tokenizer)

        function_arg_characters = function_arg_characters[:-1]
        function_arg_code = "".join(function_arg_characters)

        args_tokenizer = Tokenizer(function_arg_code)
        try:
            tokens = args_tokenizer.get_tokens()
        except:
            raise IllegalCharacter(tokenizer)

        return ListToken(tokens)

    def __repr__(self):
        out = '{'

        for item in self.items:
            out += str(item)
            out += ","

        out = out[:-1] + "}"
        return out


class TokenizerError(Exception):
    """ Represent tokenizer exceptions """
    __slots__ = ['tokenizer', 'msg']

    def __init__(self, msg, tokenizer):
        self.msg = msg
        """ Message of error """
        self.tokenizer = tokenizer
        """ Context of error """

    def __str__(self):
        """ Return information of error with information of where
            error are located
        """
        debug_info = self.tokenizer.debug_information()
        lines = debug_info['buffer'].split("\n")

        extra_information = lines[debug_info['lin']]
        extra_information += "\n" + (' '*(debug_info['col'] - 1)) + '^'

        return "{} near line {} and column {}:\n{}".format(
            self.msg,
            debug_info['lin'],
            debug_info['col'],
            extra_information
        )


class IllegalCharacter(TokenizerError):
    """ Unexpected character tokenizer error """

    def __init__(self, tokenizer):
        super().__init__("Syntax error, illegal character", tokenizer)


class Tokenizer:
    AVAILABLE_TOKENS = [
        NumberToken, BinOpToken,
        StringToken, IdentifierToken,
        ClosureToken, ListSeparatorToken,
        ListToken
    ]
    """ Represent all tokens class available """

    BLANK_SPACES = [' ', "\r"]
    """ Blank spaces to be ignored """

    __slots__ = ['buffer', 'current_pos',
                 'current_character', 'bufferlen', 'col', 'lin']

    def __init__(self, buffer):
        self.buffer = buffer
        """ Buffer that has to be processed """
        self.bufferlen = len(self.buffer)
        """ Buffer length """
        self.current_pos = -1
        """ Current buffer position """
        self.lin = 0
        """ Current line """
        self.col = 0
        """ Current column """

        self.next_character()

    def next_character(self):
        """
        Increment current buffer poisition.

        Return:
            Current character or None
        """
        self.current_pos = self.current_pos + 1

        if self.bufferlen > self.current_pos:
            self.current_character = self.buffer[self.current_pos]
        else:
            self.current_character = None

        if self.current_character == "\n":
            self.lin = self.lin + 1
            self.col = 0
        else:
            self.col = self.col + 1

        return self.current_character

    def get_current_character(self):
        """
        Get the current character.
        """
        return self.current_character

    def previous_character(self):
        """
        Decrement current buffer poisition.

        Return:
            Current character or None
        """
        self.current_pos = self.current_pos - 1
        if self.current_pos >= 0:
            self.current_character = self.buffer[self.current_pos]
        else:
            self.current_character = None

        if self.current_character == "\n":
            self.lin = self.lin - 1
            self.col = 0
        else:
            self.col = self.col - 1
        return self.current_character

    def debug_information(self):
        """
        Retrieve debug information.

        Return:
            buffer, current line, current column.
        """
        return {'buffer': self.buffer, 'lin': self.lin, 'col': self.col}

    def next_token(self):
        """
        Get next token.

        Return:
            Return next token.
        """
        while self.current_character in Tokenizer.BLANK_SPACES:
            self.next_character()

        if self.current_character is None:
            return None

        for token in Tokenizer.AVAILABLE_TOKENS:
            if token.is_match(self.current_character):
                return token.parse(self)

        raise IllegalCharacter(self)

    def get_tokens(self):
        """
        Get all tokens from buffer.

        Return:
            List of tokens.
        """

        self.current_pos = -1
        self.next_character()

        tokens = []

        token = self.next_token()

        while token is not None:
            tokens.append(token)
            token = self.next_token()

        return tokens
