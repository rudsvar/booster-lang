from dataclasses import dataclass
from expr import *
from stmt import *
import parser
from pprint import pprint
import sys


type Val = int | str


def eval(e: Expr, env: dict[str, Val]) -> Val:
    match e:
        case Int(i):
            return i
        case Str(s):
            return s
        case Var(v):
            return env[v]


def exec_one(statement: Stmt, env: dict[str, Val]):
    match statement:
        case VarDecl(v, e):
            env[v.name] = eval(e, env)
        case Print(e):
            print(eval(e, env))


def exec(statements: list[Stmt], env: dict[str, Val]):
    for statement in statements:
        exec_one(statement, env)


if __name__ == "__main__":
    input = sys.argv[1]
    prog = parser.program(input)
    env = {}
    exec(prog, env)
