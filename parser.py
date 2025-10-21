from dataclasses import dataclass
from typing import Callable, TypeVar
from expression import *
from statement import *
from copy import copy
import sys
from pprint import pprint

type Parser[T] = Callable[[str], tuple[T, str]]


@dataclass
class ParseError(Exception):
    message: str


def symbol(kw: str, input: str) -> tuple[str, str]:
    input = input.lstrip()
    if input.startswith(kw):
        return kw, input.removeprefix(kw)
    raise ParseError(f"Expected keyword {kw}, got {input[:10]}")


def take_while(check: Callable[[str], bool], input: str) -> tuple[str, str]:
    match = ""
    for c in input:
        if not check(c):
            break
        match += c
    input = input.removeprefix(match)
    return match, input


def identifier(input: str) -> tuple[str, str]:
    input = input.lstrip()
    ident, input = take_while(str.isalnum, input)
    if not ident:
        raise ParseError(f"Variable name cannot be empty")
    if not ident[0].isalpha():
        raise ParseError(f"Variable must start with an alphabetic character")
    return ident, input


def variable(input: str) -> tuple[Var, str]:
    ident, input = identifier(input)
    return Var(ident), input


def integer(input: str) -> tuple[Int, str]:
    digits, input = take_while(str.isnumeric, input)
    if not digits:
        raise ParseError(f"Expected integer, got {input[:10]}")
    if input and input[0].isalpha():
        raise ParseError("Integer cannot be followed by alphabetic character")
    return Int(int(digits)), input


def string_literal(input: str) -> tuple[StrLit, str]:
    _, input = symbol('"', input)
    str_lit, input = take_while(lambda c: c != '"', input)
    _, input = symbol('"', input)
    return StrLit(str_lit), input


T = TypeVar("T")


def any_of(parsers: list[Parser[T]], input: str) -> tuple[T, str]:
    for parser in parsers:
        try:
            return parser(input)
        except ParseError:
            pass
    raise ParseError("No parsers matched")


def expression(input: str) -> tuple[Expr, str]:
    input = input.lstrip()
    return any_of([variable, integer, string_literal, subexpression, add, mul], input)


def subexpression(input: str) -> tuple[Expr, str]:
    _, input = symbol("(", input)
    e, input = expression(input)
    _, input = symbol(")", input)
    return e, input


def add(input: str) -> tuple[Expr, str]:
    _, input = symbol("+", input)
    e1, input = expression(input)
    e2, input = expression(input)
    return Add(e1, e2), input


def mul(input: str) -> tuple[Expr, str]:
    _, input = symbol("*", input)
    e1, input = expression(input)
    e2, input = expression(input)
    return Mul(e1, e2), input


def variable_declaration(input: str) -> tuple[VarDecl, str]:
    _, input = symbol("let", input)
    v, input = identifier(input)
    _, input = symbol("=", input)
    e, input = expression(input)
    _, input = symbol(";", input)
    return VarDecl(v, e), input


def print_statement(input: str) -> tuple[Print, str]:
    _, input = symbol("print", input)
    e, input = expression(input)
    _, input = symbol(";", input)
    return Print(e), input


def block(input: str) -> tuple[Block, str]:
    _, input = symbol("{", input)
    stmts, input = statements(input)
    _, input = symbol("}", input)
    return Block(stmts), input


def statement(input: str) -> tuple[Stmt, str]:
    return any_of([variable_declaration, print_statement, block], input)


def many(parser: Parser[T], input: str) -> tuple[list[T], str]:
    results = []
    while True:
        try:
            result, input = parser(input)
            results.append(result)
        except ParseError:
            break
    return results, input


def statements(input: str) -> tuple[list[Stmt], str]:
    return many(statement, input)


def parse_program(input: str) -> list[Stmt]:
    stmts, input = statements(input)
    if input:
        raise ParseError(f'Expected end of input, got "{input[:10]}"')
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
        program = parse_program(input)
        pprint(program)
    except ParseError as e:
        print(e.message)


if __name__ == "__main__":
    main()
