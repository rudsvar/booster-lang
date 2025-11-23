from dataclasses import dataclass
from expression import Expr, Var

type Stmt = VarDecl | Assignment | Print | Block | If | FunDef | Return


@dataclass
class VarDecl:
    v: str
    e: Expr


@dataclass
class Assignment:
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


@dataclass
class FunDef:
    name: str
    params: list[str]
    body: Block


@dataclass
class Return:
    expr: Expr | None
