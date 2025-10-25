from dataclasses import dataclass

type Expr = Int | StrLit | Var | Add | Sub | Mul | Div


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
class Add:
    e1: Expr
    e2: Expr


@dataclass
class Sub:
    e1: Expr
    e2: Expr


@dataclass
class Mul:
    e1: Expr
    e2: Expr


@dataclass
class Div:
    e1: Expr
    e2: Expr
