from dataclasses import dataclass
from typing import Any, Callable
from expression import *
from statement import *
from pprint import pprint
import sys


@dataclass
class ParseException(BaseException):
    message: str
    line: int
    column: int


@dataclass
class Parser:
    input: str
    pos: int = 0
    line: int = 1
    column: int = 1
    has_consumed: bool = False

    def peek(self) -> str:
        if not self.input:
            raise ParseException("Unexpected end of input", self.line, self.column)
        return self.input[0]

    def sat(self, check: Callable[[str], bool]) -> str:
        c = self.peek()
        # Check if check is satisfied
        if not check(c):
            raise ParseException(
                f"Check {check.__name__}('{c}') failed", self.line, self.column
            )
        # Remove c from input
        self.input = self.input[1:]
        self.pos += 1
        self.has_consumed = True
        if c == "\n":
            # Go to the next line, and remember to reset column
            self.line += 1
            self.column = 1
        else:
            # Go to the next column
            self.column += 1
        return c

    def zero_or_more(self, check: Callable[[str], bool]) -> str:
        chars = ""
        while True:
            try:
                chars += self.sat(check)
            except ParseException:
                break
        return chars

    def one_or_more(self, check: Callable[[str], bool]) -> str:
        chars = self.zero_or_more(check)
        if not chars:
            raise ParseException(
                f"Expected some {check.__name__}", self.line, self.column
            )
        return chars

    def digits(self) -> str:
        return self.one_or_more(str.isdigit)

    def alphas(self) -> str:
        return self.one_or_more(str.isalpha)

    def alnums(self) -> str:
        return self.one_or_more(str.isalnum)

    def whitespace(self) -> str:
        return self.zero_or_more(str.isspace)

    def identifier(self) -> str:
        try:
            alpha = self.sat(str.isalpha)
            alnums = self.zero_or_more(lambda c: c.isalnum() or c == "_")
            return alpha + alnums
        except ParseException as e:
            raise ParseException(
                f"Expected identifier: {e.message}", self.line, self.column
            )

    def exactly(self, target: str) -> str:
        actual = self.input[: len(target)]
        try:
            s = ""
            for target_c in target:
                s += self.sat(lambda c: c == target_c)
            return s
        except ParseException as e:
            if actual:
                raise ParseException(
                    f'Expected "{target}", got "{actual}"', self.line, self.column
                )
            else:
                raise ParseException(
                    f'Expected "{target}": {e.message}', self.line, self.column
                )

    def symbol(self, target: str) -> str:
        s = self.exactly(target)
        _ = self.whitespace()
        return s

    def keyword(self, keyword: str) -> str:
        self_input = self.input
        try:
            s = self.exactly(keyword)
            if self.input and self.peek().isalnum():
                raise ParseException(
                    f'Keyword "{s}" cannot be followed by "{self.peek()}"',
                    self.line,
                    self.column,
                )
            _ = self.whitespace()
            return s
        except ParseException as e:
            # Allow keyword failures to continue
            self.input = self_input
            self.has_consumed = False
            raise e

    def one_of(self, parsers: list[Callable[[], Any]]) -> Any:
        self.has_consumed = False
        for parser in parsers:
            try:
                return parser()
            except ParseException as e:
                if self.has_consumed:
                    raise e
                continue
        raise ParseException(
            f"None of {[p.__name__ for p in parsers]} matched", self.line, self.column
        )

    def optional(self, parser) -> Any | None:
        self.has_consumed = False
        try:
            return parser()
        except ParseException as e:
            if self.has_consumed:
                raise e
            return None

    def separated_by(self, parser, separator: str) -> list[Any]:
        elements = []
        while True:
            try:
                element = parser()
                elements.append(element)
                _ = self.symbol(separator)
            except ParseException:
                break
        return elements


class ExpressionParser(Parser):

    def int(self) -> Int:
        i = Int(int(self.digits()))
        if self.input and self.peek().isalpha():
            raise ParseException(
                f'Int cannot be followed by alphabetic character at "{i.i}{self.peek()}"',
                self.line,
                self.column,
            )
        self.whitespace()
        return i

    def var(self) -> Var:
        ident = self.identifier()
        self.whitespace()
        return Var(ident)

    def var_or_function_call(self) -> Var | FunCall:
        v = self.var()
        # Check if it's a function call
        if self.input and self.peek() == "(":
            _ = self.symbol("(")
            args = self.separated_by(self.expr, ",")
            _ = self.symbol(")")
            return FunCall(v.name, args)
        # Wasn't a function call, return identifier as variable
        return v

    def str_lit(self) -> StrLit:
        _ = self.exactly('"')
        s = self.zero_or_more(lambda c: c != '"')
        _ = self.exactly('"')
        _ = self.whitespace()
        return StrLit(s)

    def bool(self) -> Bool:
        self_input = self.input
        try:
            true = lambda: self.keyword("true")
            false = lambda: self.keyword("false")
            b = self.one_of([true, false])
            _ = self.whitespace()
            return Bool(b == "true")
        except ParseException as e:
            self.has_consumed = False
            self.input = self_input
            raise e

    def lst(self) -> List:
        _ = self.symbol("[")
        elements = []
        # Try to get first element
        element = self.optional(self.expr)
        if element:
            elements.append(element)
        # Further elements require comma
        while True:
            try:
                _ = self.symbol(",")
                elements.append(self.expr())
            except ParseException:
                break
        _ = self.symbol("]")
        return List(elements)

    def expr(self) -> Expr:
        input_at_start = self.input
        pos_at_start = self.pos
        try:
            return self.one_of(
                [
                    self.int,
                    self.str_lit,
                    self.bool,
                    self.var_or_function_call,
                    self.bin_op,
                    self.sub_expr,
                    self.lst,
                ]
            )
        except ParseException as e:
            pos_diff = self.pos - pos_at_start + 1
            raise ParseException(
                f'Failed to parse expression at "{input_at_start[:pos_diff]}": {e.message}',
                self.line,
                self.column,
            )

    def sub_expr(self) -> Expr:
        _ = self.symbol("(")
        e = self.expr()
        _ = self.symbol(")")
        return e

    def bin_op(self) -> Expr:
        op = self.one_of(
            [
                lambda: self.keyword("+"),
                lambda: self.keyword("-"),
                lambda: self.keyword("*"),
                lambda: self.keyword("/"),
                lambda: self.keyword("=="),
            ]
        )
        e1 = self.expr()
        e2 = self.expr()
        return BinOp(op, e1, e2)


class StatementParser(ExpressionParser):

    def var_decl(self) -> VarDecl:
        _ = self.keyword("let")
        v = self.var_or_function_call()
        _ = self.symbol("=")
        e = self.expr()
        _ = self.symbol(";")
        return VarDecl(v.name, e)

    def assignment(self) -> Assignment:
        v = self.var_or_function_call()
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
                self.var_decl,
                self.if_statement,
                self.print,
                self.block,
                self.function_definition,
                self.return_statement,
                self.assignment,
            ]
        )

    def statements(self) -> list[Stmt]:
        stmts = []
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


class ProgramParser(StatementParser):

    def program(self) -> list[Stmt]:
        self.whitespace()
        stmts = self.statements()
        if self.input:
            raise ParseException(
                f"Expected end of input at {self.input[:20]}", self.line, self.column
            )
        return stmts


def main():
    input = sys.argv[1]
    try:
        with open(input) as f:
            input = f.read()
    except FileNotFoundError:
        pass
    # Parse and execute
    try:
        parser = ProgramParser(input)
        program = parser.program()
        pprint(program)
    except ParseException as e:
        print(f"{e.message} at {e.line}:{e.column}")


if __name__ == "__main__":
    main()
