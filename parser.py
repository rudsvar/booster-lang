import re
from statement import *


def parse_program(input: str) -> list[Statement]:
    statements: list[Statement] = []
    for line in re.split(r"\n|;", input.strip(";")):
        tokens: list[str] = line.strip().split()
        statement = parse_statement(tokens)
        statements.append(statement)
    return statements


def parse_value(s: str) -> Value:
    return int(s) if s.isdigit() else s


def parse_statement(tokens: list[str]) -> Statement:
    print(f"\033[2;30m{tokens}\033[0m")
    match tokens:
        case []:
            return Nop()
        case ["set", x, y]:
            return Set(x, parse_value(y))
        case ["print", x]:
            return Print(parse_value(x))
        case ["if", x, op, y, "then", *rest]:
            x = parse_value(x)
            y = parse_value(y)
            statement = parse_statement(rest)
            return If(x, op, y, statement)
    return Nop()


if __name__ == "__main__":
    import sys

    program = parse_program(sys.stdin.read())
    print(program)
