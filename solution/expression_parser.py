from dataclasses import dataclass
from base_parser import *
import sys
from pprint import pprint

type Expr = int | bool | str | Var | BinOp | List | FunCall


@dataclass
class Var:
    name: str


@dataclass
class BinOp:
    op: str
    e1: Expr
    e2: Expr


@dataclass
class List:
    elements: list[Expr]


@dataclass
class FunCall:
    name: str
    args: list[Expr]


class ExpressionParser(BaseParser):

    def parse_int(self) -> int:
        """
        Parses digits, converts them to an integer, and consumes whitespace. Optionally checks the next character to ensure it's not alphabetic.

        >>> parser = ExpressionParser("42")
        >>> parser.parse_int()
        42
        """
        i = int(self.parse_digits())
        # Not strictly required, but ensures we get a proper error if a variable starts with a digit
        if self.input and self.peek().isalpha():
            self.fail(
                f'Int cannot be followed by alphabetic character at "{i}{self.peek()}"'
            )
        self.parse_whitespace()
        return i

    def parse_var(self) -> Var:
        """
        Parses a single variable name and consumes whitespace.

        >>> parser = ExpressionParser("foo")
        >>> parser.parse_var()
        Var(name='foo')
        """
        ident = self.parse_identifier()
        self.parse_whitespace()
        return Var(ident)

    def parse_str_lit(self) -> str:
        """
        Parses a single string literal like "hello world" followed by whitespace. The input includes quotes (or another character if you want), but the output should not.

        >>> parser = ExpressionParser('"hello"')
        >>> parser.parse_str_lit()
        'hello'
        """
        _ = self.parse_string('"')
        s = self.parse_until('"')
        _ = self.parse_string('"')
        _ = self.parse_whitespace()
        return s

    def parse_bool(self) -> bool:
        """
        Parses a single boolean value like true or false followed by whitespace. You can choose other names if you want.

        >>> parser = ExpressionParser("true")
        >>> parser.parse_bool()
        True
        """
        b = self.one_of_strings(["true", "false"])
        return b == "true"

    def parse_list(self) -> List:
        """
        Parses expressions separated by comma and surrounded by [ and ], followed by whitespace.

        >>> parser = ExpressionParser("[1, 2, 3]")
        >>> parser.parse_list()
        List(elements=[1, 2, 3])
        """
        _ = self.parse_symbol("[")
        elements = self.separated_by(self.parse_expr, ",")
        _ = self.parse_symbol("]")
        _ = self.parse_whitespace()
        return List(elements)

    def parse_bin_op(self) -> Expr:
        """
        Parses an operator like `+` followed by two more expressions. Using prefix-notation like `+ 2 3` makes parsing much simpler.

        >>> parser = ExpressionParser("add 2 3")
        >>> parser.parse_bin_op()
        BinOp(op='add', e1=2, e2=3)
        """
        op = self.one_of_strings(["add", "sub", "mul", "div", "eq", "neq"])
        e1 = self.parse_expr()
        e2 = self.parse_expr()
        return BinOp(op, e1, e2)

    def parse_function_call(self) -> FunCall:
        """
        Parses a function call. This can look like `call foo(arg1, arg2)`. The keyword `call` is added for fun. Optionally, you can make it not require parentheses nor comma.

        >>> parser = ExpressionParser("call foo(1, 2)")
        >>> parser.parse_function_call()
        FunCall(name='foo', args=[1, 2])
        """
        # Keyword `call`
        _ = self.parse_keyword("call")
        # Function name
        v = self.parse_var()
        # Argument list
        _ = self.parse_symbol("(")
        args = self.separated_by(self.parse_expr, ",")
        _ = self.parse_symbol(")")
        return FunCall(v.name, args)

    def parse_sub_expr(self) -> Expr:
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

    def parse_expr(self) -> Expr:
        """
        Parses any kind of expression.

        >>> parser = ExpressionParser("42")
        >>> parser.parse_expr()
        42
        """
        try:
            return self.one_of(
                [
                    self.parse_int,
                    self.parse_str_lit,
                    self.parse_bool,
                    self.parse_function_call,
                    self.parse_bin_op,
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
