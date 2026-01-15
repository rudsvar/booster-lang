from dataclasses import dataclass
from parser.expression import *

type Stmt = VarDef | Assignment | Print | Block | If | FunDef | Return


@dataclass
class VarDef:
    v: str
    e: Expr


@dataclass
class Assignment:
    v: str
    e: Expr


@dataclass
class Print:
    e: Expr


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
        _ = self.keyword("let")
        v = self.var()
        _ = self.symbol("=")
        e = self.expr()
        _ = self.symbol(";")
        return VarDef(v.name, e)

    def assignment(self) -> Assignment:
        v = self.var()
        _ = self.symbol("=")
        e = self.expr()
        _ = self.symbol(";")
        return Assignment(v.name, e)

    def print(self) -> Print:
        self_input = self.input
        try:
            _ = self.keyword("print")
            e = self.expr()
            _ = self.symbol(";")
            return Print(e)
        except ParseException as e:
            self.has_consumed = False
            self.input = self_input
            raise e

    def statement(self) -> Stmt:
        return self.one_of(
            [
                self.var_def,
                self.if_statement,
                self.print,
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
        _ = self.symbol("{")
        stmts = self.statements()
        _ = self.symbol("}")
        return Block(stmts)

    def if_statement(self) -> If:
        _ = self.keyword("if")
        condition = self.expr()
        then_branch = self.block()
        else_branch = self.optional(lambda: self.else_branch())
        return If(condition, then_branch, else_branch)

    def else_branch(self) -> Block:
        _ = self.keyword("else")
        return self.block()

    def function_definition(self) -> FunDef:
        _ = self.keyword("fun")
        name = self.identifier()
        _ = self.symbol("(")
        parameters = self.separated_by(self.identifier, ",")
        _ = self.symbol(")")
        body = self.block()
        return FunDef(name, parameters, body)

    def return_statement(self) -> Return:
        _ = self.keyword("return")
        e = self.optional(self.expr)
        _ = self.symbol(";")
        return Return(e)
