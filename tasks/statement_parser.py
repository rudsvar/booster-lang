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

    def parse_shout(self) -> Shout:
        raise NotImplementedError("parse_shout is not implemented")

    def parse_var_def(self) -> VariableDefinition:
        raise NotImplementedError("parse_var_def is not implemented")

    def parse_assignment(self) -> Assignment:
        raise NotImplementedError("parse_assignment is not implemented")

    def parse_statements(self) -> list[Statement]:
        return self.zero_or_more(self.parse_statement)

    def parse_block(self) -> Block:
        _ = self.parse_symbol("{")
        stmts = self.parse_statements()
        _ = self.parse_symbol("}")
        return Block(stmts)

    def parse_if(self) -> If:
        raise NotImplementedError("parse_if is not implemented")

    def else_branch(self) -> Block:
        _ = self.parse_keyword("else")
        return self.parse_block()

    def parse_whilst(self) -> Whilst:
        raise NotImplementedError("parse_whilst is not implemented")

    def parse_function_definition(self) -> FunctionDefinition:
        raise NotImplementedError("parse_function_definition is not implemented")

    def parse_return_statement(self) -> Return:
        _ = self.parse_keyword("return")
        e = self.optional(self.parse_expr)
        _ = self.parse_symbol(";")
        return Return(e)

    def parse_statement(self) -> Statement:
        try:
            return self.one_of(
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
