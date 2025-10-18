from dataclasses import dataclass


@dataclass
class Int:
    i: int


@dataclass
class Var:
    name: str


@dataclass
class Str:
    s: str


type Expr = Int | Str | Var | Add | Mul


@dataclass
class Add:
    e1: Expr
    e2: Expr


@dataclass
class Mul:
    e1: Expr
    e2: Expr
