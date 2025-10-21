from dataclasses import dataclass
from expression import Expr, Var

type Stmt = VarDecl | Print | Block


@dataclass
class VarDecl:
    v: str
    e: Expr


@dataclass
class Print:
    e: Expr


@dataclass
class Block:
    statements: list[Stmt]
