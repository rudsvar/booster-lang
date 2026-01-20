"""
A parser with basic low-level parsing functionality.
"""

from dataclasses import dataclass
from typing import Callable, TypeVar

"""
The output of a parser.
"""
Output = TypeVar("Output")

"""
Describes the type signature of parser functions.
"""
type ParserFun[Output] = Callable[[], Output]


@dataclass
class ParseException(BaseException):
    message: str
    line: int
    column: int


@dataclass
class BaseParser:
    """
    A general parser with low-level parser functions.

    To use it, construct a new parser and call the parser methods to gradually consume and parse the input.
    The remaining input is part of the state of the parser and will automatically be updated.

    >>> p = BaseParser("foo")
    >>> p.peek()
    'f'

    >>> p = BaseParser("foo")
    >>> p.parse_identifier()
    'foo'

    >>> p = BaseParser('hello world')
    >>> p.parse_string('hello')
    'hello'

    >>> p = BaseParser('{ }')
    >>> p.parse_symbol('{')
    '{'

    >>> p = BaseParser('let x = 10;')
    >>> p.parse_keyword('let')
    'let'

    >>> p = BaseParser("def")
    >>> p.one_of_strings(["abc", "def"])
    'def'

    Methods with double underscores are not needed for these tasks and can be ignored.
    """

    input: str
    pos: int = 0
    line: int = 1
    column: int = 1
    has_consumed: bool = False

    def __init__(self, input: str):
        """
        Constructs a new parser with the provided input and defaults for everything else.

        >>> p = BaseParser("input")
        """
        self.input = input

    def peek(self) -> str:
        """
        Looks at the next character without consuming input.

        >>> p = BaseParser("input")
        >>> p.peek()
        'i'
        """
        if not self.input:
            raise ParseException("Unexpected end of input", self.line, self.column)
        return self.input[0]

    def __sat(self, check: Callable[[str], bool]) -> str:
        c = self.peek()
        # Check if check is satisfied
        if not check(c):
            raise ParseException(
                f"Check {check.__name__}('{c}') failed", self.line, self.column
            )
        # Remove c from input
        self.input = self.input[1:]
        self.pos += 1
        self.has_consumed = True
        if c == "\n":
            # Go to the next line, and remember to reset column
            self.line += 1
            self.column = 1
        else:
            # Go to the next column
            self.column += 1
        return c

    def __zero_or_more_chars(self, check: Callable[[str], bool]) -> str:
        chars = ""
        while True:
            try:
                chars += self.__sat(check)
            except ParseException:
                break
        return chars

    def __one_or_more_chars(self, check: Callable[[str], bool]) -> str:
        chars = self.__zero_or_more_chars(check)
        if not chars:
            raise ParseException(
                f"Expected some {check.__name__}", self.line, self.column
            )
        return chars

    def parse_until(self, target: str):
        """
        Parses until the target string is reached, but does not consume the target itself.

        >>> p = BaseParser('hello!')
        >>> p.parse_until('!')
        'hello'
        """
        return self.__zero_or_more_chars(lambda s: s != target)

    def parse_digits(self) -> str:
        """
        Parses a string of digits 0-9 like `12345`.

        >>> p = BaseParser('123')
        >>> p.parse_digits()
        '123'
        """
        return self.__one_or_more_chars(str.isdigit)

    def parse_alphabetics(self) -> str:
        """
        Parses a string of alphabetic characters like `hello`.

        >>> p = BaseParser('abc')
        >>> p.parse_alphabetics()
        'abc'
        """
        return self.__one_or_more_chars(str.isalpha)

    def parse_alphanumerics(self) -> str:
        """
        Parses a string of alphabetic characters.

        >>> p = BaseParser('abc123')
        >>> p.parse_alphanumerics()
        'abc123'
        """
        return self.__one_or_more_chars(str.isalnum)

    def parse_whitespace(self):
        """
        Consumes and discards whitespace.

        >>> p = BaseParser(' \\n\\t test')
        >>> assert p.input == ' \\n\\t test'
        >>> p.parse_whitespace()
        >>> assert p.input == 'test'
        """
        self.__zero_or_more_chars(str.isspace)

    def parse_identifier(self) -> str:
        """
        Parses a name-like string with alphanumeric characters and underscores.

        Parses a string of alphabetic characters.

        >>> p = BaseParser('my_var3')
        >>> p.parse_identifier()
        'my_var3'
        """
        try:
            alpha = self.__sat(lambda c: c.isalpha() or c == "_")
            alnums = self.__zero_or_more_chars(lambda c: c.isalnum() or c == "_")
            identifier = alpha + alnums
            if not identifier:
                self.fail("Identifier cannot be empty")
            return alpha + alnums
        except ParseException as e:
            self.fail(f"Expected identifier: {e.message}")

    def parse_string(self, target: str) -> str:
        """
        Parses an exact string.

        >>> p = BaseParser('some string')
        >>> some = p.parse_string('some ')
        >>> assert p.input == 'string'
        >>> some
        'some '
        """
        actual = self.input[: len(target)]
        # self.has_consumed = False
        try:
            s = ""
            for target_char in target:
                s += self.__sat(lambda c: c == target_char)
            return s
        except ParseException as e:
            if actual:
                raise ParseException(
                    f'Expected "{target}", got "{actual}"', self.line, self.column
                )
            else:
                raise ParseException(
                    f'Expected "{target}": {e.message}', self.line, self.column
                )

    def parse_symbol(self, target: str) -> str:
        """
        Parses an exact string followed by optional whitespace.
        Useful for symbol like parentheses, brackets and braces.

        >>> p = BaseParser('{ }')
        >>> left_brace = p.parse_symbol('{')
        >>> assert p.input == '}'
        >>> left_brace
        '{'
        """
        s = self.parse_string(target)
        _ = self.parse_whitespace()
        return s

    def parse_keyword(self, keyword: str) -> str:
        """
        Parses an exact string followed by optional whitespace, but does fail irrecoverably like parse_symbol.
        If parse_symbol
        This is useful to try reading the entire keyword and checking if we're just looking at the prefix of a variable or not.

        >>> p = BaseParser('{ }')
        >>> left_brace = p.parse_symbol('{')
        >>> assert p.input == '}'
        >>> left_brace
        '{'

        In this case, parse_symbol would fail irrecoverably since it consumes 'let' from the input, while parse_keyword allows one_of to try more alternatives.

        >>> p = BaseParser('lettuce')
        >>> p.one_of([lambda: p.parse_keyword('let'), lambda: p.parse_keyword('lettuce')])
        'lettuce'
        """
        self_input = self.input
        try:
            s = self.parse_string(keyword)
            if self.input and self.peek().isalnum():
                raise ParseException(
                    f'Keyword "{s}" cannot be followed by "{self.peek()}"',
                    self.line,
                    self.column,
                )
            _ = self.parse_whitespace()
            return s
        except ParseException as e:
            # Allow keyword failures to continue
            self.input = self_input
            self.has_consumed = False
            raise e

    def zero_or_more(self, parser: ParserFun[Output]) -> list[Output]:
        """
        Runs the provided parser zero or more times and returns the list of parsed values.

        >>> p = BaseParser('hellohelloworld')
        >>> p.zero_or_more(lambda: p.parse_string('hello'))
        ['hello', 'hello']
        """
        stmts: list[Output] = []
        while True:
            try:
                self.has_consumed = False
                stmts.append(parser())
            except ParseException as e:
                if self.has_consumed:
                    raise e
                break
        return stmts

    def one_of(self, parsers: list[ParserFun[Output]]) -> Output:
        """
        Tries to run each of the parsers until one succeeds. If one fails and has consumed input, we abort and return the error.

        >>> p = BaseParser('let')
        >>> let = lambda: p.parse_keyword('let')
        >>> call = lambda: p.parse_keyword('call')
        >>> p.one_of([let, call])
        'let'

        >>> p = BaseParser('call')
        >>> let = lambda: p.parse_keyword('let')
        >>> call = lambda: p.parse_keyword('call')
        >>> p.one_of([let, call])
        'call'
        """
        self.has_consumed = False
        for parser in parsers:
            try:
                return parser()
            except NotImplementedError:
                continue
            except ParseException as e:
                if self.has_consumed:
                    raise e
                continue
        raise ParseException(
            f"None of {[p.__name__ for p in parsers]} matched", self.line, self.column
        )

    def one_of_strings(self, strings: list[str]) -> str:
        """
        Tries to parse one of the provided strings

        >>> p = BaseParser('foo')
        >>> p.one_of_strings(['foo', 'bar'])
        'foo'

        >>> p = BaseParser('bar')
        >>> p.one_of_strings(['foo', 'bar'])
        'bar'
        """
        try:
            parsers = list(map(lambda s: lambda: self.parse_keyword(s), strings))
            return self.one_of(parsers)
        except ParseException:
            raise ParseException(f"None of {strings} matched", self.line, self.column)

    def optional(self, parser: ParserFun[Output]) -> Output | None:
        """
        Tries to run the provided parser, but returns None if it fails. If it fails after having consumed input it will throw an error as usual.

        >>> p = BaseParser('foo')
        >>> p.optional(lambda: p.parse_string('foo'))
        'foo'

        >>> p = BaseParser('bar')
        >>> p.optional(lambda: p.parse_string('foo'))
        """
        self.has_consumed = False
        try:
            return parser()
        except ParseException as e:
            if self.has_consumed:
                raise e
            return None

    def separated_by(self, parser: ParserFun[Output], separator: str) -> list[Output]:
        """
        Runs the provided parser zero or more times separated by the provided separator, and returns the list of parsed values

        >>> p = BaseParser("123,456,789")
        >>> p.separated_by(p.parse_digits, ',')
        ['123', '456', '789']
        """
        elements: list[Output] = []
        while True:
            try:
                element = parser()
                elements.append(element)
                _ = self.parse_symbol(separator)
            except ParseException:
                break
        return elements

    def fail(self, message: str):
        raise ParseException(message, self.line, self.column)
