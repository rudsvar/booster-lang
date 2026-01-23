from dataclasses import dataclass
from base_parser import *
import sys
from pprint import pprint

type Expression = int | bool | str | Variable | BinaryOperation | list[
    Expression
] | FunctionCall


@dataclass
class Variable:
    name: str


@dataclass
class BinaryOperation:
    op: str
    e1: Expression
    e2: Expression


@dataclass
class FunctionCall:
    name: str
    args: list[Expression]


class ExpressionParser(BaseParser):
    """A parser for expressions that extends `BaseParser`."""

    def parse_int(self) -> int:
        """
        Parses digits using parsers from BaseParser (self.parse_*), converts them to an integer, and consumes whitespace.

        Hint: You can convert a string to an integer with int(my_string)

        >>> parser = ExpressionParser("42")
        >>> parser.parse_int()
        42
        """
        raise NotImplementedError("parse_int is not implemented")

    def parse_var(self) -> Variable:
        """
        Parses a single variable name and consumes whitespace.

        >>> parser = ExpressionParser("foo")
        >>> parser.parse_var()
        Variable(name='foo')
        """
        raise NotImplementedError("parse_var is not implemented")

    def parse_string_literal(self) -> str:
        """
        Parses a single string literal like "hello world" followed by whitespace. The input includes quotes (or another character if you want), but the output should not.

        >>> parser = ExpressionParser('"hello"')
        >>> parser.parse_string_literal()
        'hello'
        """
        raise NotImplementedError("parse_string_literal is not implemented")

    def parse_bool(self) -> bool:
        """
        Parses a single boolean value like true or false followed by whitespace. You can choose other names if you want.

        >>> parser = ExpressionParser("true")
        >>> parser.parse_bool()
        True
        """
        raise NotImplementedError("parse_bool is not implemented")

    def parse_binary_operation(self) -> Expression:
        """
        Parses an operator like `+` followed by two expressions. Using prefix-notation like `+ 2 3` makes parsing much simpler.
        You can rename the operators to any string you want.

        >>> parser = ExpressionParser("add 2 3")
        >>> parser.parse_binary_operation()
        BinaryOperation(op='add', e1=2, e2=3)
        """
        raise NotImplementedError("parse_binary_operation is not implemented")

    def parse_list(self) -> list[Expression]:
        """
        Parses expressions separated by comma and surrounded by [ and ], followed by whitespace.

        >>> parser = ExpressionParser('[1, a, "abc"]')
        >>> parser.parse_list()
        [1, Variable(name='a'), 'abc']
        """
        _ = self.parse_symbol("[")
        elements = self.separated_by(self.parse_expr, ",")
        _ = self.parse_symbol("]")
        _ = self.parse_whitespace()
        return elements

    def parse_function_call(self) -> FunctionCall:
        """
        Parses a function call. This can look like `call foo(arg1, arg2)`. The keyword `call` is added for fun. Optionally, you can make it not require parentheses nor comma.

        >>> parser = ExpressionParser("call foo(1, 2)")
        >>> parser.parse_function_call()
        FunctionCall(name='foo', args=[1, 2])
        """
        raise NotImplementedError("parse_function_call is not implemented")

    def parse_sub_expr(self) -> Expression:
        """
        Parses an expression surrounded by parentheses.

        >>> parser = ExpressionParser("(42)")
        >>> parser.parse_sub_expr()
        42
        """
        _ = self.parse_symbol("(")
        e = self.parse_expr()
        _ = self.parse_symbol(")")
        return e

    def parse_expr(self) -> Expression:
        """
        Parses any kind of expression.

        >>> parser = ExpressionParser("42")
        >>> parser.parse_expr()
        42
        """
        try:
            return self.any(
                [
                    self.parse_int,
                    self.parse_string_literal,
                    self.parse_bool,
                    self.parse_function_call,
                    self.parse_binary_operation,
                    self.parse_sub_expr,
                    self.parse_list,
                    self.parse_var,
                ]
            )
        except ParseException as e:
            self.fail(f"Failed to parse expression: {e.message}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python expression_parser.py <expression>")
        sys.exit(1)

    try:
        parser = ExpressionParser(sys.argv[1])
        expr = parser.parse_expr()
        pprint(expr)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
