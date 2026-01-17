from dataclasses import dataclass

from interpreter.interpret_exception import InterpretException
from interpreter.value import Value


@dataclass
class Env:
    """Example of how to implement an environment type"""

    scopes: list[dict[str, Value]]

    def __init__(self):
        """Initialize an environment with one initial top-level scope"""
        self.scopes = [{}]

    def open_scope(self):
        """Open a new, empty scope"""
        self.scopes.append({})

    def close_scope(self):
        """Close the nearest scope"""
        self.scopes.pop()

    def inner_scope(self) -> dict[str, Value]:
        """Get a reference to the closest/nearest/inner scope"""
        return self.scopes[-1]

    def top_level_scope(self) -> dict[str, Value]:
        """Get a reference to the top level scope"""
        return self.scopes[0]

    def define_var(self, var: str, value: Value):
        """Define a new variable in the nearest scope"""
        inner_scope = self.inner_scope()
        inner_scope[var] = value

    def lookup_var(self, var: str) -> Value:
        """Look up a variable's value from the environment"""
        for scope in reversed(self.scopes):
            val = scope.get(var)
            if val is not None:
                return val
        raise InterpretException(f'Undefined variable "{var}"')

    def assign_var(self, var: str, value: Value):
        """Assign a new value to an existing variable"""
        for scope in reversed(self.scopes):
            if scope.get(var) is not None:
                scope[var] = value
                return
        raise InterpretException(f'Undefined variable "{var}"')
