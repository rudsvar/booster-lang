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
        _ = self.parse_keyword("shout")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return Shout(e)

    def parse_var_def(self) -> VariableDefinition:
        """
        Parses a variable definition statement. Requires a semicolon at the end.

        >>> parser = StatementParser("let x = 42;")
        >>> parser.parse_var_def()
        VariableDefinition(var_name='x', expr=IntLit(value=42))
        """
        _ = self.parse_keyword("let")
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return VariableDefinition(v.name, e)

    def parse_assignment(self) -> Assignment:
        """
        Parses a variable assignment statement. Requires a semicolon at the end.

        >>> parser = StatementParser("x = 100;")
        >>> parser.parse_assignment()
        Assignment(var_name='x', expr=IntLit(value=100))
        """
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return Assignment(v.name, e)

    def parse_statements(self) -> list[Statement]:
        return self.zero_or_more(self.parse_statement)

    def parse_block(self) -> Block:
        """
        Parses a block of statements surrounded by braces. Does not require a semicolon.

        >>> parser = StatementParser("{ let x = 10; shout x; }")
        >>> parser.parse_block()
        Block(statements=[VariableDefinition(var_name='x', expr=IntLit(value=10)), Shout(expr=Variable(name='x'))])
        """
        _ = self.parse_symbol("{")
        stmts = self.parse_statements()
        _ = self.parse_symbol("}")
        return Block(stmts)

    def parse_if(self) -> If:
        """
        Parses an if statement with an optional else branch. Does not require a semicolon.

        >>> parser = StatementParser("if true { shout 1; }")
        >>> parser.parse_if()
        If(condition=BoolLit(value=True), then_block=Block(statements=[Shout(expr=IntLit(value=1))]), else_block=None)
        """
        _ = self.parse_keyword("if")
        condition = self.parse_expr()
        then_branch = self.parse_block()
        else_branch = self.optional(lambda: self.else_branch())
        return If(condition, then_branch, else_branch)

    def else_branch(self) -> Block:
        _ = self.parse_keyword("else")
        return self.parse_block()

    def parse_whilst(self) -> Whilst:
        """
        Parses a while loop statement. Does not require a semicolon.

        >>> parser = StatementParser("whilst true { shout 1; }")
        >>> parser.parse_whilst()
        Whilst(condition=BoolLit(value=True), body=Block(statements=[Shout(expr=IntLit(value=1))]))
        """
        _ = self.parse_keyword("whilst")
        condition = self.parse_expr()
        body = self.parse_block()
        return Whilst(condition, body)

    def parse_function_definition(self) -> FunctionDefinition:
        """
        Parses a function definition. Does not require a semicolon.

        >>> parser = StatementParser("fun add(x, y) { return add x y; }")
        >>> parser.parse_function_definition()
        FunctionDefinition(name='add', params=['x', 'y'], body=Block(statements=[Return(expr=BinaryOperation(op='add', e1=Variable(name='x'), e2=Variable(name='y')))]))
        """
        _ = self.parse_keyword("fun")
        name = self.parse_identifier()
        _ = self.parse_symbol("(")
        parameters = self.separated_by(self.parse_identifier, ",")
        _ = self.parse_symbol(")")
        body = self.parse_block()
        return FunctionDefinition(name, parameters, body)

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
