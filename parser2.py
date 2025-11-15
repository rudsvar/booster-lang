from dataclasses import dataclass
from typing import Callable


@dataclass
class ParseException(BaseException):
    message: str
    line: int
    column: int


@dataclass
class Parser:
    input: str
    line: int = 1
    column: int = 1
    has_consumed: bool = False

    def peek(self) -> str:
        if not self.input:
            raise ParseException("No more input", self.line, self.column)
        return self.input[0]

    def sat(self, check: Callable[[str], bool]) -> str:
        c = self.peek()
        # Check if check is satisfied
        if not check(c):
            raise ParseException(
                f"{check.__name__}('{c}') failed", self.line, self.column
            )
        # Remove c from input
        self.input = self.input[1:]
        self.has_consumed = True
        if c == "\n":
            # Go to the next line, and remember to reset column
            self.line += 1
            self.column = 1
        else:
            # Go to the next column
            self.column += 1
        return c

    def many(self, check: Callable[[str], bool]) -> str:
        chars = ""
        while True:
            try:
                chars += self.sat(check)
            except ParseException:
                break
        return chars

    def some(self, check: Callable[[str], bool], tag: str) -> str:
        chars = self.many(check)
        if not chars:
            raise ParseException(f"Expected some {tag}", self.line, self.column)
        return chars

    def digits(self) -> str:
        return self.some(str.isdigit, "digits")

    def alphas(self) -> str:
        return self.some(str.isalpha, "alphas")

    def exactly(self, target: str) -> str:
        actual = self.input[: len(target)]
        try:
            s = ""
            for target_c in target:
                s += self.sat(lambda c: c == target_c)
            return s
        except:
            raise ParseException(
                f'Expected "{target}", got "{actual}..."', self.line, self.column
            )
