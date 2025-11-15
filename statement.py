from dataclasses import dataclass
from expression import Expr, Var

type Stmt = VarDecl | Print | Block | If


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


@dataclass
class If:
    condition: Expr
    then_block: Block
    else_block: Block | None
