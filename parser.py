from dataclasses import dataclass
from typing import Callable, TypeVar
from expression import *
from statement import *
from functools import wraps
import sys
from pprint import pprint

T = TypeVar("T")

type Parser[T] = Callable[[], T]


@dataclass
class ParseError(Exception):
    message: str


log = open("parser_log.txt", mode="w")
log_depth = 0


def debug_parser(func: Callable):
    @wraps(func)
    def log_call(*args, **kwargs):
        global log_depth
        log.write(f"{4*log_depth*" "}{func.__qualname__} ")
        for arg in args:
            if hasattr(arg, "__name__"):
                log.write(f"{arg.__name__} ")
            else:
                log.write(f"{arg} ")
        log.write("\n")
        try:
            log_depth += 1
            result = func(*args, **kwargs)
            log_depth -= 1
            log.write(f"{4*log_depth*" "}-> {result}\n")
            return result
        except ParseError as e:
            log_depth -= 1
            log.write(f"{4*log_depth*" "}{e}\n")
            raise e

    return log_call


@dataclass
class Input:
    data: str

    def preview(self) -> str:
        return self.data[: self.data.find("\n")]

    def lstrip(self):
        """Remove leading whitespace"""
        self.data = self.data.lstrip()

    @debug_parser
    def symbol(self, symbol: str) -> str:
        """"""
        self.lstrip()
        if not self.data.startswith(symbol):
            raise ParseError(f'Expected symbol "{symbol}", got "{self.preview()}"')
        self.data = self.data.removeprefix(symbol)
        return symbol

    @debug_parser
    def take_while(self, check: Callable[[str], bool]) -> str:
        match = ""
        for c in self.data:
            if not check(c):
                break
            match += c
        self.data = self.data.removeprefix(match)
        return match

    @debug_parser
    def identifier(self) -> str:
        self.lstrip()
        ident = self.take_while(str.isalnum)
        if not ident:
            raise ParseError(f'Expected variable, got "{self.preview()}"')
        if not ident[0].isalpha():
            raise ParseError(f'Expected alphabetic character, got "{self.preview()}"')
        return ident

    @debug_parser
    def variable(self) -> Var:
        return Var(self.identifier())

    @debug_parser
    def integer(self) -> Int:
        digits = self.take_while(str.isnumeric)
        if not digits:
            raise ParseError(f"Expected integer, got {self.preview()}")
        if self.data and self.data[0].isalpha():
            raise ParseError(
                f"Integer cannot be followed by alphabetic character, but got {self.preview()}"
            )
        return Int(int(digits))

    @debug_parser
    def string_literal(self) -> StrLit:
        _ = self.symbol('"')
        str_lit = self.take_while(lambda c: c != '"')
        _ = self.symbol('"')
        return StrLit(str_lit)

    @debug_parser
    def one_of(self, *parsers: Parser[T]) -> T:
        original_data = self.data
        for parser in parsers:
            try:
                result = parser()
                return result
            except ParseError as e:
                self.data = original_data
                pass
        raise ParseError(
            f"Expected one of {[p.__qualname__ for p in parsers]}, but got {self.preview()}"
        )

    @debug_parser
    def factor(self) -> Expr:
        self.lstrip()
        return self.one_of(
            self.integer, self.string_literal, self.variable, self.subexpression
        )

    @debug_parser
    def term(self) -> Expr:
        factor = self.factor()
        if self.optional(lambda: self.symbol("*")):
            term2 = self.term()
            return Mul(factor, term2)
        if self.optional(lambda: self.symbol("/")):
            term2 = self.term()
            return Div(factor, term2)
        return factor

    @debug_parser
    def expression(self) -> Expr:
        term = self.term()
        if self.optional(lambda: self.symbol("+")):
            expression2 = self.expression()
            return Mul(term, expression2)
        if self.optional(lambda: self.symbol("-")):
            expression2 = self.expression()
            return Sub(term, expression2)
        return term

    @debug_parser
    def subexpression(self) -> Expr:
        _ = self.symbol("(")
        e = self.expression()
        _ = self.symbol(")")
        return e

    @debug_parser
    def variable_declaration(self) -> VarDecl:
        try:
            _ = self.symbol("let")
            v = self.identifier()
            _ = self.symbol("=")
            e = self.expression()
            _ = self.symbol(";")
            return VarDecl(v, e)
        except ParseError:
            raise ParseError(f"Expected variable declaration, but got {self.preview()}")

    @debug_parser
    def print_statement(self) -> Print:
        _ = self.symbol("print")
        _ = self.symbol("(")
        e = self.expression()
        _ = self.symbol(")")
        _ = self.symbol(";")
        return Print(e)

    @debug_parser
    def block(self) -> Block:
        _ = self.symbol("{")
        stmts = self.statements()
        _ = self.symbol("}")
        return Block(stmts)

    @debug_parser
    def statement(self) -> Stmt:
        return self.one_of(
            self.variable_declaration, self.print_statement, self.block, self.expression
        )

    @debug_parser
    def statements(self) -> list[Stmt]:
        stmts = []
        while True:
            try:
                stmts.append(self.statement())
            except ParseError:
                break
        return stmts

    @debug_parser
    def many(self, parser: Parser[T]):
        results = []
        while True:
            # Store a backup of the state
            self_data = self.data
            try:
                results.append(parser())
            except ParseError:
                # Restore the backup
                self.data = self_data
                break
        return results

    @debug_parser
    def optional(self, parser: Parser[T]):
        self_data = self.data
        try:
            return parser()
        except ParseError:
            self.data = self_data
            return None


@debug_parser
def parse_program(input_str: str) -> list[Stmt]:
    input = Input(input_str)
    stmts = input.statements()
    if input.data:
        print(f"{stmts}")
        raise ParseError(f'Expected end of input, got "{input.preview()}"')
    return stmts


def main():
    input = sys.argv[1]
    try:
        with open(input) as f:
            input = f.read()
    except FileNotFoundError:
        pass
    # Parse and execute
    try:
        program = parse_program(input)
        pprint(program)
    except ParseError as e:
        print(e.message)


if __name__ == "__main__":
    main()
