from dataclasses import dataclass

type Expr = Int | StrLit | Bool | Var | BinOp | List | FunCall


@dataclass
class Int:
    i: int


@dataclass
class Var:
    name: str


@dataclass
class StrLit:
    s: str


@dataclass
class Bool:
    b: bool


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
