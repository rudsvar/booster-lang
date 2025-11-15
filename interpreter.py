from dataclasses import dataclass
from expression import *
from statement import *
from parser import *
import sys


type Value = int | float | str | bool | list[Value]

type Env = list[dict[str, Value]]


@dataclass
class InterpretException(Exception):
    message: str


def lookup(env: Env, var: str) -> Value:
    for scope in reversed(env):
        val = scope.get(var)
        if val is not None:
            return val
    raise InterpretException(f'Undefined variable "{var}"')


def eval(e: Expr, env: Env) -> Value:
    match e:
        case Int(i):
            return i
        case StrLit(s):
            return s
        case Bool(b):
            return b
        case Var(v):
            return lookup(env, v)
        case List(elements):
            return map(lambda e: eval(e, env), elements)
        case Add(e1, e2):
            v1 = eval(e1, env)
            v2 = eval(e2, env)
            if type(v1) == int and type(v2) == int:
                return int(v1) + int(v2)
            if type(v1) == str and type(v2) == str:
                return str(v1) + str(v2)
            raise InterpretException(f"Cannot add {v1} and {v2}")
        case Sub(e1, e2):
            v1 = eval(e1, env)
            v2 = eval(e2, env)
            if type(v1) == int and type(v2) == int:
                return int(v1) - int(v2)
            raise InterpretException(f"Cannot subtract {v1} and {v2}")
        case Mul(e1, e2):
            v1 = eval(e1, env)
            v2 = eval(e2, env)
            if type(v1) == int and type(v2) == int:
                return int(v1) * int(v2)
            raise InterpretException(f"Cannot multiply {v1} and {v2}")
        case Div(e1, e2):
            v1 = eval(e1, env)
            v2 = eval(e2, env)
            if type(v1) == int and type(v2) == int:
                return int(v1) / int(v2)
            raise InterpretException(f"Cannot divide {v1} and {v2}")
        case _:
            raise InterpretException("eval not implemented for " + str(e))


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
        case If(condition, then_block, else_block):
            condition = eval(condition, env)
            if condition:
                exec_one(then_block, env)
            elif else_block:
                exec_one(else_block, env)
        case _:
            raise InterpretException("exec not implemented for " + str(statement))


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
    except InterpretException as e:
        print(e.message)
