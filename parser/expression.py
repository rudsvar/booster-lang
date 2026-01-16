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

    def int(self) -> Int:
        i = Int(int(self.digits()))
        if self.input and self.peek().isalpha():
            raise ParseException(
                f'Int cannot be followed by alphabetic character at "{i.value}{self.peek()}"',
                self.line,
                self.column,
            )
        self.whitespace()
        return i

    def var(self) -> Var:
        ident = self.identifier()
        self.whitespace()
        return Var(ident)

    def function_call(self) -> FunCall:
        # Keyword `call`
        _ = self.keyword("call")
        # Function name
        v = self.var()
        # Argument list
        _ = self.symbol("(")
        args = self.separated_by(self.expr, ",")
        _ = self.symbol(")")
        return FunCall(v.name, args)

    def str_lit(self) -> StrLit:
        _ = self.string('"')
        s = self.zero_or_more(lambda c: c != '"')
        _ = self.string('"')
        _ = self.whitespace()
        return StrLit(s)

    def bool(self) -> Bool:
        self_input = self.input
        try:
            true = lambda: self.keyword("true")
            false = lambda: self.keyword("false")
            b = self.one_of([true, false])
            _ = self.whitespace()
            return Bool(b == "true")
        except ParseException as e:
            self.has_consumed = False
            self.input = self_input
            raise e

    def lst(self) -> List:
        _ = self.symbol("[")
        elements: list[Expr] = []
        # Try to get first element
        element = self.optional(self.expr)
        if element:
            elements.append(element)
        # Further elements require comma
        while True:
            try:
                _ = self.symbol(",")
                elements.append(self.expr())
            except ParseException:
                break
        _ = self.symbol("]")
        return List(elements)

    def expr(self) -> Expr:
        input_at_start = self.input
        pos_at_start = self.pos
        try:
            return self.one_of(
                [
                    self.int,
                    self.str_lit,
                    self.bool,
                    self.function_call,
                    self.bin_op,
                    self.sub_expr,
                    self.lst,
                    self.var,
                ]
            )
        except ParseException as e:
            pos_diff = self.pos - pos_at_start + 1
            raise ParseException(
                f'Failed to parse expression at "{input_at_start[:pos_diff]}": {e.message}',
                self.line,
                self.column,
            )

    def sub_expr(self) -> Expr:
        _ = self.symbol("(")
        e = self.expr()
        _ = self.symbol(")")
        return e

    def bin_op(self) -> Expr:
        op = self.one_of(
            [
                lambda: self.keyword("+"),
                lambda: self.keyword("-"),
                lambda: self.keyword("*"),
                lambda: self.keyword("/"),
                lambda: self.keyword("=="),
            ]
        )
        e1 = self.expr()
        e2 = self.expr()
        return BinOp(op, e1, e2)
