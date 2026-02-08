from dataclasses import dataclass
from typing import Any

type Statement = Skip | Print | VarDef | Inc | Dec | Mul | Label | Goto | If | Exit | Fun | Call | Return

"""
An expression can only be a number or a variable.
"""
type Expression = int | str


@dataclass
class Skip:
    pass


@dataclass
class Print:
    value: Any


@dataclass
class VarDef:
    name: str
    value: Any


@dataclass
class Inc:
    left: str
    right: Any


@dataclass
class Dec:
    left: str
    right: Any


@dataclass
class Mul:
    left: str
    right: Any


@dataclass
class Label:
    name: str


@dataclass
class Goto:
    label: str


@dataclass
class If:
    left: Expression
    operator: str
    right: Expression
    statement: Statement


@dataclass
class Exit:
    pass


@dataclass
class Fun:
    name: str
    params: list[str]


@dataclass
class Call:
    name: str
    args: list[Any]


@dataclass
class Return:
    pass
