"""
Values that expressions can be evaluated to.
These mostly use standard Python types to make operations on them easier.
"""

from statement_parser import FunctionDef

type Value = int | str | bool | list[Value] | FunctionDef | None
