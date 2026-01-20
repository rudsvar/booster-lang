from statement_parser import *
import sys
from pprint import pprint


class ProgramParser(StatementParser):

    def parse_program(self) -> list[Statement]:
        """Parses a list of statements, but does not allow trailing input"""
        self.parse_whitespace()
        stmts = self.parse_statements()
        if self.input:
            raise ParseException(
                f"Expected end of input at {self.input[:20]}", self.line, self.column
            )
        return stmts


if __name__ == "__main__":

    def read_input(input_path: str) -> str:
        """Try to read file, otherwise treat input as code string"""
        try:
            with open(input_path) as f:
                return f.read()
        except FileNotFoundError:
            return input_path

    if len(sys.argv) < 2:
        print("Usage: python program_parser.py <file_or_code>")
        sys.exit(1)

    try:
        code = read_input(sys.argv[1])
        parser = ProgramParser(code)
        program = parser.parse_program()
        pprint(program)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
