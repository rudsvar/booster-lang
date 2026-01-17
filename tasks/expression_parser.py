from dataclasses import dataclass
from base_parser import *

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
        raise NotImplementedError("TODO")

    def parse_var(self) -> Var:
        raise NotImplementedError("TODO")

    def parse_function_call(self) -> FunCall:
        raise NotImplementedError("TODO")

    def parse_str_lit(self) -> StrLit:
        raise NotImplementedError("TODO")

    def parse_bool(self) -> Bool:
        raise NotImplementedError("TODO")

    def parse_list(self) -> List:
        raise NotImplementedError("TODO")

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
        raise NotImplementedError("TODO")

    def parse_bin_op(self) -> Expr:
        raise NotImplementedError("TODO")
