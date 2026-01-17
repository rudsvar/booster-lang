import sys
import argparse
from pprint import pprint
from interpreter.interpret_exception import InterpretException
from parser.program import ProgramParser
from parser.expression import ParseException
from interpreter.interpreter import Env
from interpreter import interpreter


def read_input(input_path: str) -> str:
    """Try to read file, otherwise treat input as code string"""
    try:
        with open(input_path) as f:
            return f.read()
    except FileNotFoundError:
        return input_path


def cmd_parse(args: argparse.Namespace) -> None:
    code = read_input(args.input)
    parser = ProgramParser(code)
    program = parser.parse_program()
    pprint(program)


def cmd_run(args: argparse.Namespace) -> None:
    code = read_input(args.input)
    parser = ProgramParser(code)
    program = parser.parse_program()

    env = Env()
    interpreter.exec_program(program, env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="booster-lang")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="Parse and print AST")
    parse_parser.add_argument("input", help="File or code string")
    parse_parser.set_defaults(func=cmd_parse)

    run_parser = subparsers.add_parser("run", help="Parse and execute")
    run_parser.add_argument("input", help="File or code string")
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()

    try:
        args.func(args)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
    except InterpretException as e:
        print("error:", e.message)
        sys.exit(1)
