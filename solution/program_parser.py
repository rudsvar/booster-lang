from .statement_parser import *


class ProgramParser(StatementParser):

    def parse_program(self) -> list[Stmt]:
        """Parses a list of statements, but does not allow trailing input"""
        self.parse_whitespace()
        stmts = self.parse_statements()
        if self.input:
            raise ParseException(
                f"Expected end of input at {self.input[:20]}", self.line, self.column
            )
        return stmts
