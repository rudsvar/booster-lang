from dataclasses import dataclass
from expression_parser import *

type Stmt = VarDef | Assignment | Shout | Block | If | Whilst | FunDef | Return


@dataclass
class VarDef:
    var_name: str
    expr: Expr


@dataclass
class Assignment:
    var_name: str
    expr: Expr


@dataclass
class Shout:
    expr: Expr


@dataclass
class Block:
    statements: list[Stmt]


@dataclass
class If:
    condition: Expr
    then_block: Block
    else_block: Block | None


@dataclass
class Whilst:
    condition: Expr
    body: Block


@dataclass
class FunDef:
    name: str
    params: list[str]
    body: Block


@dataclass
class Return:
    expr: Expr | None


class StatementParser(ExpressionParser):

    def parse_var_def(self) -> VarDef:
        raise NotImplementedError("TODO")

    def parse_assignment(self) -> Assignment:
        raise NotImplementedError("TODO")

    def parse_shout(self) -> Shout:
        raise NotImplementedError("TODO")

    def parse_statements(self) -> list[Stmt]:
        raise NotImplementedError("TODO")

    def parse_block(self) -> Block:
        raise NotImplementedError("TODO")

    def parse_if(self) -> If:
        raise NotImplementedError("TODO")

    def else_branch(self) -> Block:
        raise NotImplementedError("TODO")

    def parse_whilst(self) -> Whilst:
        raise NotImplementedError("TODO")

    def parse_function_definition(self) -> FunDef:
        raise NotImplementedError("TODO")

    def parse_return_statement(self) -> Return:
        raise NotImplementedError("TODO")

    def parse_statement(self) -> Stmt:
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
