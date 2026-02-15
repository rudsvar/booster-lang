from dataclasses import dataclass

type Statement = Skip | Print | Let | Inc | Dec | Mul | Swap | Label | Goto | If | Exit | Proc | Call | Return

"""
An expression can only be a number or a variable.
"""
type Expression = int | str


@dataclass
class Skip:
    pass


@dataclass
class Print:
    expr: Expression


@dataclass
class Let:
    var: str
    expr: Expression


@dataclass
class Inc:
    var: str
    expr: Expression


@dataclass
class Dec:
    var: str
    expr: Expression


@dataclass
class Mul:
    var: str
    expr: Expression


@dataclass
class Swap:
    var1: str
    var2: str


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
class Proc:
    name: str
    params: list[str]


@dataclass
class Call:
    name: str
    args: list[Expression]


@dataclass
class Return:
    pass
