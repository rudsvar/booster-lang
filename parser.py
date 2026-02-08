from statement import *


def parse_program(input: str) -> list[Statement]:
    """
    Splits the source code into "lines" by semicolon, and each line into tokens by whitespace.
    """
    statements: list[Statement] = []
    for line in input.rstrip(";").split(";"):
        tokens: list[str] = line.strip().split()
        statement = parse_statement(tokens)
        statements.append(statement)
    return statements


def parse_expr(s: str) -> Expression:
    """A value can either be a number or a variable."""
    return int(s) if s.isdigit() else s


def parse_statement(tokens: list[str]) -> Statement:
    """Pattern matches to convert a line of tokens into a statement."""
    debug_log(str(tokens))
    match tokens:
        case []:
            return Skip()
        case ["print", x]:
            return Print(parse_expr(x))
        case ["set", x, y]:
            return VarDef(x, parse_expr(y))
        case ["halt"]:
            return Halt()
        case ["inc", x, y]:
            return Inc(x, parse_expr(y))
        case ["label", label]:
            return Label(label)
        case ["goto", label]:
            return Goto(label)
        case ["if", x, op, y, "then", *rest]:
            x = parse_expr(x)
            y = parse_expr(y)
            statement = parse_statement(rest)
            return If(x, op, y, statement)
        case ["if", x, op, y, "then", *rest]:
            x = parse_expr(x)
            y = parse_expr(y)
            statement = parse_statement(rest)
            return If(x, op, y, statement)
    raise ValueError(f"No matches for {tokens}")


DEBUG = False


def debug_log(msg: str) -> None:
    if DEBUG:
        print(f"\033[2;30mtokens={msg}\033[0m")


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
