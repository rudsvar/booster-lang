from dataclasses import dataclass
from expression import *
from statement import *
from parser import *
import sys


type Value = int | str

type Env = list[dict[str, Value]]


@dataclass
class EvalException(Exception):
    message: str


def lookup(env: Env, var: str) -> Value:
    for scope in reversed(env):
        val = scope.get(var)
        if val:
            return val
    raise EvalException(f'Variable "{var}" not defined')


def eval(e: Expr, env: Env) -> Value:
    match e:
        case Int(i):
            return i
        case StrLit(s):
            return s
        case Var(v):
            return lookup(env, v)
        case Add(e1, e2):
            return int(eval(e1, env)) + int(eval(e2, env))
        case Mul(e1, e2):
            return int(eval(e1, env)) * int(eval(e2, env))
        case _:
            raise EvalException("eval not implemented for " + str(e))


def exec_one(statement: Stmt, env: Env):
    match statement:
        case VarDecl(v, e):
            scope = env[-1]
            scope[v] = eval(e, env)
        case Print(e):
            print(eval(e, env))
        case Block(statements):
            env.append({})
            exec(statements, env)
            env.pop()
        case _:
            raise EvalException("exec not implemented for " + str(statement))


def exec(statements: list[Stmt], env: Env):
    for statement in statements:
        exec_one(statement, env)


if __name__ == "__main__":
    # Read file or use arg as program
    input = sys.argv[1]
    try:
        with open(input) as f:
            input = f.read()
    except FileNotFoundError:
        pass

    # Parse and execute
    try:
        parser = ProgramParser(input)
        program = parser.program()
        env = [{}]
        exec(program, env)
    except ParseException as e:
        print(f"{e.message} at {e.line}:{e.column}")
    except EvalException as e:
        print(e.message)
