from dataclasses import dataclass
from expression_parser import *
import sys
from pprint import pprint

type Statement = Shout | VariableDefinition | Assignment | Block | If | Whilst | FunctionDefinition | Return


@dataclass
class Shout:
    expr: Expression


@dataclass
class VariableDefinition:
    var_name: str
    expr: Expression


@dataclass
class Assignment:
    var_name: str
    expr: Expression


@dataclass
class Block:
    statements: list[Statement]


@dataclass
class If:
    condition: Expression
    then_block: Block
    else_block: Block | None


@dataclass
class Whilst:
    condition: Expression
    body: Block


@dataclass
class FunctionDefinition:
    name: str
    params: list[str]
    body: Block


@dataclass
class Return:
    expr: Expression | None


class StatementParser(ExpressionParser):
    """A parser for statements that extends `ExpressionParser`.

    Note: Some statements like `shout`, `let`, `return`, and assignments require a semicolon at the end.
    Block and control flow statements (if, whilst, fun) do not require a semicolon.
    """

    def parse_shout(self) -> Shout:
        """
        Parses a shout statement that prints a value. Requires a semicolon at the end.

        >>> parser = StatementParser("shout 42;")
        >>> parser.parse_shout()
        Shout(expr=IntLit(value=42))
        """
        raise NotImplementedError("parse_shout is not implemented")

    def parse_var_def(self) -> VariableDefinition:
        """
        Parses a variable definition statement. Requires a semicolon at the end.

        >>> parser = StatementParser("let x = 42;")
        >>> parser.parse_var_def()
        VariableDefinition(var_name='x', expr=IntLit(value=42))
        """
        raise NotImplementedError("parse_var_def is not implemented")

    def parse_assignment(self) -> Assignment:
        """
        Parses a variable assignment statement. Requires a semicolon at the end.

        >>> parser = StatementParser("x = 100;")
        >>> parser.parse_assignment()
        Assignment(var_name='x', expr=IntLit(value=100))
        """
        raise NotImplementedError("parse_assignment is not implemented")

    def parse_statements(self) -> list[Statement]:
        return self.zero_or_more(self.parse_statement)

    def parse_block(self) -> Block:
        """
        Parses a block of statements surrounded by braces. Does not require a semicolon.

        >>> parser = StatementParser("{ let x = 10; shout x; }")
        >>> parser.parse_block()
        Block(statements=[VariableDefinition(var_name='x', expr=IntLit(value=10)), Shout(expr=Variable(name='x'))])
        """
        raise NotImplementedError("parse_block is not implemented")

    def parse_if(self) -> If:
        """
        Parses an if statement with an optional else branch. Does not require a semicolon.

        >>> parser = StatementParser("if true { shout 1; }")
        >>> parser.parse_if()
        If(condition=BoolLit(value=True), then_block=Block(statements=[Shout(expr=IntLit(value=1))]), else_block=None)
        """
        raise NotImplementedError("parse_if is not implemented")

    def else_branch(self) -> Block:
        raise NotImplementedError("else_branch is not implemented")

    def parse_whilst(self) -> Whilst:
        """
        Parses a while loop statement. Does not require a semicolon.

        >>> parser = StatementParser("whilst true { shout 1; }")
        >>> parser.parse_whilst()
        Whilst(condition=BoolLit(value=True), body=Block(statements=[Shout(expr=IntLit(value=1))]))
        """
        raise NotImplementedError("parse_whilst is not implemented")

    def parse_function_definition(self) -> FunctionDefinition:
        """
        Parses a function definition. Does not require a semicolon.

        >>> parser = StatementParser("fun add(x, y) { return add x y; }")
        >>> parser.parse_function_definition()
        FunctionDefinition(name='add', params=['x', 'y'], body=Block(statements=[Return(expr=BinaryOperation(op='add', e1=Variable(name='x'), e2=Variable(name='y')))]))
        """
        raise NotImplementedError("parse_function_definition is not implemented")

    def parse_return_statement(self) -> Return:
        """
        Parses a return statement. The return value can be optional. Requires a semicolon at the end.

        >>> parser = StatementParser("return 42;")
        >>> parser.parse_return_statement()
        Return(expr=IntLit(value=42))
        """
        _ = self.parse_keyword("return")
        e = self.optional(self.parse_expr)
        _ = self.parse_symbol(";")
        return Return(e)

    def parse_statement(self) -> Statement:
        try:
            return self.any(
                [
                    self.parse_var_def,
                    self.parse_if,
                    self.parse_whilst,
                    self.parse_shout,
                    self.parse_block,
                    self.parse_function_definition,
                    self.parse_return_statement,
                    self.parse_assignment,
                ]
            )
        except ParseException as e:
            self.fail(f"Failed to parse statement: {e.message}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python statement_parser.py <statement>")
        sys.exit(1)

    try:
        parser = StatementParser(sys.argv[1])
        stmt = parser.parse_statement()
        pprint(stmt)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
