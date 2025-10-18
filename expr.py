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


type Expr = Int | Str | Var
