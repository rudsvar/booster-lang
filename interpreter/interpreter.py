from dataclasses import dataclass
from parser.program import *
import sys


type Value = int | float | str | bool | list[Value] | FunDef | None


@dataclass
class InterpretException(Exception):
    message: str


@dataclass
class Env:
    scopes: list[dict[str, Value]]

    def __init__(self):
        """Initialize an environment with one initial top-level scope"""
        self.scopes = [{}]

    def open_scope(self):
        """Open a new, empty scope"""
        self.scopes.append({})

    def close_scope(self):
        """Close the nearest scope"""
        self.scopes.pop()

    def inner_scope(self) -> dict[str, Value]:
        """Get a reference to the closest/nearest/inner scope"""
        return self.scopes[-1]

    def top_level_scope(self) -> dict[str, Value]:
        """Get a reference to the top level scope"""
        return self.scopes[0]

    def define(self, var: str, value: Value):
        """Define a new variable in the nearest scope"""
        inner_scope = self.inner_scope()
        inner_scope[var] = value

    def lookup(self, var: str) -> Value:
        """Look up a variable's value from the environment"""
        for scope in reversed(self.scopes):
            val = scope.get(var)
            if val is not None:
                return val
        raise InterpretException(f'Undefined variable "{var}"')

    def assign(self, var: str, value: Value):
        """Assign a new value to an existing variable"""
        for scope in reversed(self.scopes):
            if scope.get(var) is not None:
                scope[var] = value
                return
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
            return env.lookup(v)
        case List(elements):
            return [eval(e, env) for e in elements]
        case BinOp(op, e1, e2):
            v1 = eval(e1, env)
            v2 = eval(e2, env)
            match op:
                case "+" if type(v1) == int and type(v2) == int:
                    return int(v1) + int(v2)
                case "+" if type(v1) == str and type(v2) == str:
                    return str(v1) + str(v2)
                case "-" if type(v1) == int and type(v2) == int:
                    return int(v1) - int(v2)
                case "*" if type(v1) == int and type(v2) == int:
                    return int(v1) * int(v2)
                case "/" if type(v1) == int and type(v2) == int:
                    return int(v1) / int(v2)
                case "==" if type(v1) == type(v2):
                    return v1 == v2
                case _:
                    raise InterpretException(
                        f"Operator {op} does not work on {v1} and {v2}"
                    )
        case FunCall(name, args):
            # Look up function in scope
            f = env.lookup(name)
            if type(f) != FunDef:
                raise InterpretException(f"{f} is not callable")

            # Check argument length matches parameter length
            params = f.params
            if len(params) != len(args):
                raise InterpretException(
                    f"{name} expects {len(params)} arguments, but got {len(args)}"
                )

            # Pass a custom env with two scopes:
            # 1. The top level scope
            # 2. A fresh one to bind arguments to parameter names
            function_env: Env = Env()
            function_env.scopes = [env.top_level_scope()]
            function_env.open_scope()
            for param, arg in zip(params, args):
                # Put parameters in the fresh scope
                function_env.define(param, eval(arg, env))

            # Run body with function env
            return exec_one(f.body, function_env)
        case _:
            raise InterpretException("eval not implemented for " + str(e))


def exec_one(statement: Stmt, env: Env) -> Value | None:
    match statement:
        case VarDef(v, e):
            env.define(v, eval(e, env))
        case Assignment(v, e):
            env.assign(v, eval(e, env))
        case Print(e):
            print(eval(e, env))
        case Block(statements):
            env.open_scope()
            return_value = exec(statements, env)
            env.close_scope()
            return return_value
        case If(condition, then_block, else_block):
            condition = eval(condition, env)
            if condition:
                return exec_one(then_block, env)
            elif else_block:
                return exec_one(else_block, env)
        case FunDef(name, _, _) as f:
            env.define(name, f)
        case Return(return_value):
            if return_value:
                return eval(return_value, env)
        case _:
            raise InterpretException("exec not implemented for " + str(statement))
    return None


def exec(statements: list[Stmt], env: Env) -> Value | None:
    for statement in statements:
        return_value = exec_one(statement, env)
        if return_value is not None:
            return return_value


def exec_string(input: str) -> Value | None:
    parser = ProgramParser(input)
    program = parser.program()
    env: Env = Env()
    exec(program, env)


def exec_file(path: str) -> Value | None:
    with open(path) as f:
        inp = f.read()
        exec_string(inp)


if __name__ == "__main__":
    # Read file or use arg as program
    input = sys.argv[1]
    try:
        exec_file(input)
    except FileNotFoundError:
        pass

    # Parse and execute
    try:
        exec_string(input)
    except ParseException as e:
        print(f"{e.message} at {e.line}:{e.column}")
    except InterpretException as e:
        print(e.message)
