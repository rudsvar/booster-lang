from dataclasses import dataclass
import pprint
from typing import Any, Callable, Self, TypeVar
import sys


@dataclass
class Int:
    i: int


Expr = Int


@dataclass
class VarDecl:
    v: str
    e: Expr


@dataclass
class Print:
    s: str


Stmt = VarDecl | Print


@dataclass
class ParseError(Exception):
    message: str


@dataclass
class Input:
    input: str

    def sat(self, pred: Callable[[str], bool]) -> str:
        if not self.input:
            raise ParseError("Empty input")

        c = self.input[0]
        if not pred(c):
            raise ParseError("Not satisfied")

        self.input = self.input.removeprefix(c)
        return c

    T = TypeVar("T")

    def many(self, p: Callable[[], T]) -> list[T]:
        results = []
        while True:
            try:
                results.append(p())
            except ParseError:
                break
        return results

    def some(self, p: Callable[[], T]) -> list[T]:
        results = self.many(p)
        if not results:
            raise ParseError("Expected at least one")
        return results

    def alnum(self) -> str:
        return self.sat(str.isalnum)

    def identifier(self) -> str:
        self.spaces()
        first = self.sat(str.isalpha)
        rest: list[str] = self.many(self.alnum)
        return first + "".join(rest)

    def space(self) -> str:
        return self.sat(str.isspace)

    def spaces(self) -> str:
        spaces = self.many(self.space)
        return "".join(spaces)

    def pad(self, p: Callable[[], T]):
        self.spaces()
        return p()

    def digit(self) -> str:
        return self.tag("Expected digit", lambda: self.sat(str.isdecimal))

    def int(self) -> int:
        return int(self.pad(self.digit))

    def string(self, s: str) -> str:
        input = self.input.removeprefix(s)
        if len(self.input) - len(input) != len(s):
            raise ParseError(f'Expected string "{s}" but got "{self.input[:5]}"')
        self.input = input
        return s

    def symbol(self, s: str) -> str:
        return self.tag(
            f'Expected symbol "{s}" but got "{self.input[:5]}"',
            lambda: self.pad(lambda: self.string(s)),
        )

    def number(self) -> Expr:
        i = self.int()
        return Int(i)

    def vardecl(self) -> Stmt:
        self.symbol("let")
        ident = self.identifier()
        self.symbol("=")
        expr = self.number()
        return VarDecl(ident, expr)

    def tag(self, msg: str, p: Callable[[], T]) -> T:
        try:
            return p()
        except ParseError:
            raise ParseError(f"{msg}")

def main() -> None:
    input = Input(sys.argv[1])
    pprint.pprint(input.many(lambda: input.vardecl(); input.vardecl()))


if __name__ == "__main__":
    main()
