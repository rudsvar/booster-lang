from dataclasses import dataclass
from parser.expression import *

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
        _ = self.parse_keyword("let")
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return VarDef(v.name, e)

    def parse_assignment(self) -> Assignment:
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return Assignment(v.name, e)

    def parse_shout(self) -> Shout:
        _ = self.parse_keyword("shout")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return Shout(e)

    def parse_statements(self) -> list[Stmt]:
        return self.zero_or_more(self.parse_statement)

    def parse_block(self) -> Block:
        _ = self.parse_symbol("{")
        stmts = self.parse_statements()
        _ = self.parse_symbol("}")
        return Block(stmts)

    def parse_if(self) -> If:
        _ = self.parse_keyword("if")
        condition = self.parse_expr()
        then_branch = self.parse_block()
        else_branch = self.optional(lambda: self.else_branch())
        return If(condition, then_branch, else_branch)

    def else_branch(self) -> Block:
        _ = self.parse_keyword("else")
        return self.parse_block()

    def parse_whilst(self) -> Whilst:
        _ = self.parse_keyword("whilst")
        condition = self.parse_expr()
        body = self.parse_block()
        return Whilst(condition, body)

    def parse_function_definition(self) -> FunDef:
        _ = self.parse_keyword("fun")
        name = self.parse_identifier()
        _ = self.parse_symbol("(")
        parameters = self.separated_by(self.parse_identifier, ",")
        _ = self.parse_symbol(")")
        body = self.parse_block()
        return FunDef(name, parameters, body)

    def parse_return_statement(self) -> Return:
        _ = self.parse_keyword("return")
        e = self.optional(self.parse_expr)
        _ = self.parse_symbol(";")
        return Return(e)

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
