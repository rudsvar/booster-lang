from dataclasses import dataclass
from typing import Callable, TypeVar
from expr import *
from stmt import *
from copy import copy
import sys
from pprint import pprint

type Parser[T] = Callable[[str], tuple[T, str]]


@dataclass
class ParseError(Exception):
    message: str


def symbol(kw: str, input: str) -> tuple[str, str]:
    input = input.strip()
    if input.startswith(kw):
        return kw, input.removeprefix(kw)
    raise ParseError(f"Expected keyword {kw}, got {input[:10]}")


def variable(input: str) -> tuple[Var, str]:
    input = input.strip()
    # Count characters that match filter
    i = 0
    for c in input:
        if not c.isalnum() or c.isspace():
            break
        i += 1
    # Take matching prefix
    name = input[:i]
    # Check that it starts with an alphabetic character
    if not name or not name[0].isalpha():
        raise ParseError(
            f"Var must start with alphabetic character, but got {input[:10]}"
        )
    return Var(name), input[i:]


def integer(input: str) -> tuple[Int, str]:
    input = input.strip()

    # Take digits
    i = 0
    for c in input:
        if not c.isdigit():
            break
        i += 1

    # Take matching prefix
    digits, rest = input[:i], input[i:]

    # Make sure it's not empty
    if not digits or (rest and rest[0].isalpha()):
        raise ParseError(f"Expected integer, got {input[:10]}")

    # Make sure it's not followed by an alphabetic character
    if rest and rest[0].isalpha():
        raise ParseError(f"Integer cannot be followed by alphabetic character")

    return Int(int(digits)), rest


def string_literal(input: str) -> tuple[StrLit, str]:
    _, input = symbol('"', input)
    i = 0
    for c in input:
        if c != '"':
            i += 1
    _, input = symbol('"', input)
    return StrLit(input[:i]), input[i:]


T = TypeVar("T")


def any_of(parsers: list[Parser[T]], input: str) -> tuple[T, str]:
    for parser in parsers:
        try:
            return parser(input)
        except ParseError:
            pass
    raise ParseError("No parsers matched")


def expression(input: str) -> tuple[Expr, str]:
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
    v, input = variable(input)
    _, input = symbol("=", input)
    e, input = expression(input)
    return VarDecl(v, e), input


def print_statement(input: str) -> tuple[Print, str]:
    _, input = symbol("print", input)
    e, input = expression(input)
    return Print(e), input


def statement(input: str) -> tuple[Stmt, str]:
    stmt, input = any_of([variable_declaration, print_statement], input)
    _, input = symbol(";", input)
    return stmt, input


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


def program(input: str) -> list[Stmt]:
    stmts, input = statements(input)
    if input:
        raise ParseError(f"Expected end of input, got {input[:10]}")
    return stmts


if __name__ == "__main__":
    input = sys.argv[1]
    try:
        with open(input) as f:
            input = f.read()
    except FileNotFoundError:
        pass
    prog = program(input)
    pprint(prog)
