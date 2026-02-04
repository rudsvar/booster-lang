from dataclasses import dataclass
from typing import Any

type Statement = Nop | Set | Print | Push | Pop | Sub | Add | Label | Jmp | Jeq | Jlt | Fun | Call | Return | If

type Value = int | str


@dataclass
class Nop:
    pass


@dataclass
class Set:
    name: str
    value: Any


@dataclass
class Print:
    value: Any


@dataclass
class Push:
    value: Any


@dataclass
class Pop:
    name: str


@dataclass
class Sub:
    left: str
    right: Any


@dataclass
class Add:
    left: str
    right: Any


@dataclass
class Label:
    name: str


@dataclass
class Jmp:
    label: str


@dataclass
class Jeq:
    left: Any
    right: Any
    label: str


@dataclass
class Jlt:
    left: Any
    right: Any
    label: str


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
    name: str
    value: Any


@dataclass
class If:
    left: Value
    operator: str
    right: Value
    statement: Statement
