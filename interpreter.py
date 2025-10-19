from dataclasses import dataclass
from expression import *
from statement import *
import parser
from pprint import pprint
import sys


type Value = int | str


def eval(e: Expr, env: dict[str, Value]) -> Value:
    match e:
        case Int(i):
            return i
        case StrLit(s):
            return s
        case Var(v):
            return env[v]
        case Add(e1, e2):
            return int(eval(e1, env)) + int(eval(e2, env))
        case Mul(e1, e2):
            return int(eval(e1, env)) * int(eval(e2, env))
        case _:
            raise Exception("eval not implemented for " + str(e))


def exec_one(statement: Stmt, env: dict[str, Value]):
    match statement:
        case VarDecl(v, e):
            env[v.name] = eval(e, env)
        case Print(e):
            print(eval(e, env))
        case Block(statements):
            exec(statements, env)
        case _:
            raise Exception("exec not implemented for " + str(statement))


def exec(statements: list[Stmt], env: dict[str, Value]):
    for statement in statements:
        exec_one(statement, env)


if __name__ == "__main__":
    input = sys.argv[1]
    try:
        with open(input) as f:
            input = f.read()
    except FileNotFoundError:
        pass
    prog = parser.program(input)
    env = {}
    exec(prog, env)
