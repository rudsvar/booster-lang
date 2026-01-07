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
class Parser:
    input: str
    pos: int = 0
    line: int = 1
    column: int = 1
    has_consumed: bool = False

    def peek(self) -> str:
        if not self.input:
            raise ParseException("Unexpected end of input", self.line, self.column)
        return self.input[0]

    def sat(self, check: Callable[[str], bool]) -> str:
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

    def zero_or_more(self, check: Callable[[str], bool]) -> str:
        chars = ""
        while True:
            try:
                chars += self.sat(check)
            except ParseException:
                break
        return chars

    def one_or_more(self, check: Callable[[str], bool]) -> str:
        chars = self.zero_or_more(check)
        if not chars:
            raise ParseException(
                f"Expected some {check.__name__}", self.line, self.column
            )
        return chars

    def digits(self) -> str:
        return self.one_or_more(str.isdigit)

    def alphas(self) -> str:
        return self.one_or_more(str.isalpha)

    def alnums(self) -> str:
        return self.one_or_more(str.isalnum)

    def whitespace(self) -> str:
        return self.zero_or_more(str.isspace)

    def identifier(self) -> str:
        try:
            alpha = self.sat(str.isalpha)
            alnums = self.zero_or_more(lambda c: c.isalnum() or c == "_")
            return alpha + alnums
        except ParseException as e:
            raise ParseException(
                f"Expected identifier: {e.message}", self.line, self.column
            )

    def string(self, target: str) -> str:
        """Parses an exact string"""
        actual = self.input[: len(target)]
        try:
            s = ""
            for target_c in target:
                s += self.sat(lambda c: c == target_c)
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

    def symbol(self, target: str) -> str:
        """Parses an exact string followed by optional whitespace"""
        s = self.string(target)
        _ = self.whitespace()
        return s

    def keyword(self, keyword: str) -> str:
        """
        Parses an exact string followed by optional whitespace, but does not partially consume input.
        This is required to not abort parsing if a variable starts with a prefix that looks like a keyword, like `true_var`.
        """
        self_input = self.input
        try:
            s = self.string(keyword)
            if self.input and self.peek().isalnum():
                raise ParseException(
                    f'Keyword "{s}" cannot be followed by "{self.peek()}"',
                    self.line,
                    self.column,
                )
            _ = self.whitespace()
            return s
        except ParseException as e:
            # Allow keyword failures to continue
            self.input = self_input
            self.has_consumed = False
            raise e

    def one_of(self, parsers: list[ParserFun[Output]]) -> Output:
        self.has_consumed = False
        for parser in parsers:
            try:
                return parser()
            except ParseException as e:
                if self.has_consumed:
                    raise e
                continue
        raise ParseException(
            f"None of {[p.__name__ for p in parsers]} matched", self.line, self.column
        )

    def optional(self, parser: ParserFun[Output]) -> Output | None:
        self.has_consumed = False
        try:
            return parser()
        except ParseException as e:
            if self.has_consumed:
                raise e
            return None

    def separated_by(self, parser: ParserFun[Output], separator: str) -> list[Output]:
        elements: list[Output] = []
        while True:
            try:
                element = parser()
                elements.append(element)
                _ = self.symbol(separator)
            except ParseException:
                break
        return elements
