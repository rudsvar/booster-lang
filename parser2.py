from dataclasses import dataclass
from typing import Callable
import expression


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
        alpha = self.sat(str.isalpha)
        alnums = self.zero_or_more(lambda c: c.isalnum() or c == "_")
        _ = self.whitespace()
        return alpha + alnums

    def exactly(self, target: str) -> str:
        actual = self.input[: len(target)]
        try:
            s = ""
            for target_c in target:
                s += self.sat(lambda c: c == target_c)
            return s
        except:
            raise ParseException(
                f'Expected "{target}", got "{actual}"', self.line, self.column
            )

    def symbol(self, target: str) -> str:
        s = self.exactly(target)
        _ = self.whitespace()
        return s


class ExpressionParser(Parser):

    def int(self) -> expression.Int:
        i = expression.Int(int(self.digits()))
        if self.input and self.peek().isalpha():
            raise ParseException(
                "Int cannot be followed by alphabetic character", self.line, self.column
            )
        _ = self.whitespace()
        return i

    def var(self) -> expression.Var:
        v = expression.Var(self.identifier())
        _ = self.whitespace()
        return v

    def str_lit(self) -> expression.StrLit:
        _ = self.exactly('"')
        s = self.zero_or_more(lambda c: c != '"')
        _ = self.exactly('"')
        _ = self.whitespace()
        return expression.StrLit(s)

    def expr(self) -> expression.Expr:
        expr_parsers = [
            self.int,
            self.var,
            self.str_lit,
            self.add,
            self.sub,
            self.mul,
            self.div,
            self.sub_expr,
        ]
        self.has_consumed = False
        for p in expr_parsers:
            try:
                return p()
            except ParseException as e:
                if self.has_consumed:
                    raise e
                else:
                    continue
        raise ParseException(f"None of {expr_parsers} matched", self.line, self.column)

    def sub_expr(self) -> expression.Expr:
        _ = self.symbol("(")
        e = self.expr()
        _ = self.symbol(")")
        return e

    def add(self) -> expression.Add:
        _ = self.symbol("+")
        return expression.Add(self.expr(), self.expr())

    def sub(self) -> expression.Sub:
        _ = self.symbol("-")
        return expression.Sub(self.expr(), self.expr())

    def mul(self) -> expression.Mul:
        _ = self.symbol("*")
        return expression.Mul(self.expr(), self.expr())

    def div(self) -> expression.Div:
        _ = self.symbol("/")
        return expression.Div(self.expr(), self.expr())
