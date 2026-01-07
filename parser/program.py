import sys
from pprint import pprint
from parser.statement import *


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
