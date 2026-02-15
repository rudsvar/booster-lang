from statement import *
import sys


@dataclass
class ParseError(Exception):
    message: str


def parse_program(input: str) -> list[Statement]:
    """
    Splits the source code into "lines" by semicolon, and each line into tokens by whitespace.
    """
    statements: list[Statement] = []
    for line in input.removesuffix(";").split(";"):
        tokens: list[str] = line.strip().split()
        statement = parse_statement(tokens)
        debug_log(f"     parser.py | parse_statement({tokens}) = {statement}")
        statements.append(statement)
    return statements


def parse_expr(s: str) -> Expression:
    """A value can either be a number or a variable."""
    return int(s) if s.isdigit() else s


def parse_statement(tokens: list[str]) -> Statement:
    """Pattern matches to convert a line of tokens into a statement."""
    match tokens:
        case []:
            return Skip()
        case ["#", *rest]:
            return Skip()
        case ["print", x]:
            e = parse_expr(x)
            return Print(e)
        case ["let", x, y]:
            e = parse_expr(y)
            return Let(x, e)
        case ["inc", x, y]:
            e = parse_expr(y)
            return Inc(x, e)
        case ["dec", x, y]:
            e = parse_expr(y)
            return Dec(x, e)
        case ["mul", x, y]:
            e = parse_expr(y)
            return Mul(x, e)
        case ["swap", x, y]:
            return Swap(x, y)
        case ["label", label]:
            return Label(label)
        case ["goto", label]:
            return Goto(label)
        case ["if", x, op, y, "then", *rest]:
            x = parse_expr(x)
            y = parse_expr(y)
            statement = parse_statement(rest)
            return If(x, op, y, statement)
        case ["exit"]:
            return Exit()
        case ["proc", name, *params]:
            return Proc(name, params)
        case ["call", name, *args]:
            args = [parse_expr(arg) for arg in args]
            return Call(name, args)
        case ["return"]:
            return Return()
        case _:
            raise ParseError(f"No matches for '{" ".join(tokens)}'")


debug = False


def debug_log(msg: str, end: str | None = None) -> None:
    if debug:
        print(f"\033[2;30m{msg}\033[0m", file=sys.stderr, end=end)


if __name__ == "__main__":
    import argparse
    import os
    from pprint import pprint

    parser = argparse.ArgumentParser(description="Parse booster-lang programs")
    parser.add_argument("input", help="Input file or program string")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    debug = args.debug

    if os.path.isfile(args.input):
        with open(args.input, "r") as f:
            input_str = f.read()
    else:
        input_str = args.input

    try:
        program = parse_program(input_str)
        pprint(program)
    except ParseError as e:
        print(f"Parser error: {e.message}")
