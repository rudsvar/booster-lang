from dataclasses import dataclass
from typing import Self
from expr import Expr, Var


@dataclass
class VarDecl:
    v: Var
    e: Expr


@dataclass
class Print:
    e: Expr


type Stmt = VarDecl | Print | list[Stmt]
