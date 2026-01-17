"""
Values that expressions can be evaluated to.
These mostly use standard Python types to make operations on them easier.
"""

from .statement_parser import FunDef

type Value = int | str | bool | list[Value] | FunDef | None
