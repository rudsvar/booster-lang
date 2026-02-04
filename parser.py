import re
from statement import *

DEBUG = False


def debug_log(msg: str) -> None:
    if DEBUG:
        print(f"\033[2;30m{msg}\033[0m")


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
    debug_log(str(tokens))
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
    import argparse
    import os
    from pprint import pprint

    parser = argparse.ArgumentParser(description="Parse booster-lang programs")
    parser.add_argument(
        "input", nargs="?", help="Input file or program string (default: stdin)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    DEBUG = args.debug

    if args.input is None:
        input_str = __import__("sys").stdin.read()
    elif os.path.isfile(args.input):
        with open(args.input, "r") as f:
            input_str = f.read()
    else:
        input_str = args.input

    program = parse_program(input_str)
    pprint(program)
