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
    for line in input.rstrip(";").split(";"):
        tokens: list[str] = line.strip().split()
        debug_log(f"Parsing tokens {tokens} ", end="")
        statement = parse_statement(tokens)
        debug_log(f"into {statement}")
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
        case ["print", x]:
            return Print(parse_expr(x))
        case ["set", x, y]:
            return VarDef(x, parse_expr(y))
        case ["inc", x, y]:
            return Inc(x, parse_expr(y))
        case ["dec", x, y]:
            return Dec(x, parse_expr(y))
        case ["mul", x, y]:
            return Mul(x, parse_expr(y))
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
        case ["fun", name, *params]:
            return Fun(name, params)
        case ["call", name, *args]:
            args = [parse_expr(arg) for arg in args]
            return Call(name, args)
        case ["return"]:
            return Return()
    raise ParseError(f"No matches for '{" ".join(tokens)}'")


DEBUG = False


def debug_log(msg: str, end=None) -> None:
    if DEBUG:
        print(f"\033[2;30m{msg}\033[0m", file=sys.stderr, end=end)


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

    try:
        program = parse_program(input_str)
        pprint(program)
    except ParseError as e:
        print(e.message)
