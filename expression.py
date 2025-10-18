from dataclasses import dataclass


@dataclass
class Int:
    i: int


@dataclass
class Var:
    name: str


@dataclass
class StrLit:
    s: str


type Expr = Int | StrLit | Var | Add | Mul


@dataclass
class Add:
    e1: Expr
    e2: Expr


@dataclass
class Mul:
    e1: Expr
    e2: Expr
