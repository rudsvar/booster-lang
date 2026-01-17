from dataclasses import dataclass
from parser.basic import *

type Expr = Int | StrLit | Bool | Var | BinOp | List | FunCall


@dataclass
class Int:
    value: int


@dataclass
class Var:
    name: str


@dataclass
class StrLit:
    value: str


@dataclass
class Bool:
    value: bool


@dataclass
class BinOp:
    op: str
    e1: Expr
    e2: Expr


@dataclass
class List:
    elements: list[Expr]


@dataclass
class FunCall:
    name: str
    args: list[Expr]


class ExpressionParser(Parser):

    def parse_int(self) -> Int:
        i = Int(int(self.parse_digits()))
        if self.input and self.peek().isalpha():
            raise ParseException(
                f'Int cannot be followed by alphabetic character at "{i.value}{self.peek()}"',
                self.line,
                self.column,
            )
        self.parse_whitespace()
        return i

    def parse_var(self) -> Var:
        ident = self.parse_identifier()
        self.parse_whitespace()
        return Var(ident)

    def parse_function_call(self) -> FunCall:
        # Keyword `call`
        _ = self.parse_keyword("call")
        # Function name
        v = self.parse_var()
        # Argument list
        _ = self.parse_symbol("(")
        args = self.separated_by(self.parse_expr, ",")
        _ = self.parse_symbol(")")
        return FunCall(v.name, args)

    def parse_str_lit(self) -> StrLit:
        _ = self.parse_string('"')
        s = self.zero_or_more(lambda c: c != '"')
        _ = self.parse_string('"')
        _ = self.parse_whitespace()
        return StrLit(s)

    def parse_bool(self) -> Bool:
        self_input = self.input
        try:
            true = lambda: self.parse_keyword("true")
            false = lambda: self.parse_keyword("false")
            b = self.one_of([true, false])
            _ = self.parse_whitespace()
            return Bool(b == "true")
        except ParseException as e:
            self.has_consumed = False
            self.input = self_input
            raise e

    def parse_list(self) -> List:
        _ = self.parse_symbol("[")
        elements = self.separated_by(self.parse_expr, ",")
        _ = self.parse_symbol("]")
        return List(elements)

    def parse_expr(self) -> Expr:
        input_at_start = self.input
        pos_at_start = self.pos
        try:
            return self.one_of(
                [
                    self.parse_int,
                    self.parse_str_lit,
                    self.parse_bool,
                    self.parse_function_call,
                    self.parse_bin_op,
                    self.parse_sub_expr,
                    self.parse_list,
                    self.parse_var,
                ]
            )
        except ParseException as e:
            pos_diff = self.pos - pos_at_start + 1
            raise ParseException(
                f'Failed to parse expression at "{input_at_start[:pos_diff]}": {e.message}',
                self.line,
                self.column,
            )

    def parse_sub_expr(self) -> Expr:
        _ = self.parse_symbol("(")
        e = self.parse_expr()
        _ = self.parse_symbol(")")
        return e

    def parse_bin_op(self) -> Expr:
        op = self.one_of(
            [
                lambda: self.parse_keyword("add"),
                lambda: self.parse_keyword("sub"),
                lambda: self.parse_keyword("mul"),
                lambda: self.parse_keyword("div"),
                lambda: self.parse_keyword("eq"),
                lambda: self.parse_keyword("neq"),
            ]
        )
        e1 = self.parse_expr()
        e2 = self.parse_expr()
        return BinOp(op, e1, e2)
