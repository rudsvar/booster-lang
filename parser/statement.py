from dataclasses import dataclass
from parser.expression import *

type Stmt = VarDef | Assignment | Shout | Block | If | FunDef | Return


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
class FunDef:
    name: str
    params: list[str]
    body: Block


@dataclass
class Return:
    expr: Expr | None


class StatementParser(ExpressionParser):

    def var_def(self) -> VarDef:
        _ = self.parse_keyword("let")
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return VarDef(v.name, e)

    def assignment(self) -> Assignment:
        v = self.parse_var()
        _ = self.parse_symbol("=")
        e = self.parse_expr()
        _ = self.parse_symbol(";")
        return Assignment(v.name, e)

    def shout(self) -> Shout:
        self_input = self.input
        try:
            _ = self.parse_keyword("shout")
            e = self.parse_expr()
            _ = self.parse_symbol(";")
            return Shout(e)
        except ParseException as e:
            self.has_consumed = False
            self.input = self_input
            raise e

    def statement(self) -> Stmt:
        return self.one_of(
            [
                self.var_def,
                self.if_statement,
                self.shout,
                self.block,
                self.function_definition,
                self.return_statement,
                self.assignment,
            ]
        )

    def statements(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while True:
            try:
                stmts.append(self.statement())
            except ParseException as e:
                if self.has_consumed:
                    raise e
                break
        return stmts

    def block(self) -> Block:
        _ = self.parse_symbol("{")
        stmts = self.statements()
        _ = self.parse_symbol("}")
        return Block(stmts)

    def if_statement(self) -> If:
        _ = self.parse_keyword("if")
        condition = self.parse_expr()
        then_branch = self.block()
        else_branch = self.optional(lambda: self.else_branch())
        return If(condition, then_branch, else_branch)

    def else_branch(self) -> Block:
        _ = self.parse_keyword("else")
        return self.block()

    def function_definition(self) -> FunDef:
        _ = self.parse_keyword("fun")
        name = self.parse_identifier()
        _ = self.parse_symbol("(")
        parameters = self.separated_by(self.parse_identifier, ",")
        _ = self.parse_symbol(")")
        body = self.block()
        return FunDef(name, parameters, body)

    def return_statement(self) -> Return:
        _ = self.parse_keyword("return")
        e = self.optional(self.parse_expr)
        _ = self.parse_symbol(";")
        return Return(e)
