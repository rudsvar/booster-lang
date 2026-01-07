from dataclasses import dataclass
from expression import *
from statement import *
from parser import *
import sys


type Value = int | float | str | bool | list[Value] | FunDef | None

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


def assign(env: Env, var: str, value: Value):
    for scope in reversed(env):
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
            return lookup(env, v)
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
            f = lookup(env, name)
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
            function_env: Env = [env[0], {}]
            for param, arg in zip(params, args):
                # Put parameters in the fresh scope
                function_env[-1][param] = eval(arg, env)
            # Run body with function env
            return exec_one(f.body, function_env)
        case _:
            raise InterpretException("eval not implemented for " + str(e))


def exec_one(statement: Stmt, env: Env) -> Value | None:
    match statement:
        case VarDecl(v, e):
            scope = env[-1]
            scope[v] = eval(e, env)
        case Assignment(v, e):
            assign(env, v, eval(e, env))
        case Print(e):
            print(eval(e, env))
        case Block(statements):
            env.append({})
            return_value = exec(statements, env)
            env.pop()
            return return_value
        case If(condition, then_block, else_block):
            condition = eval(condition, env)
            if condition:
                return exec_one(then_block, env)
            elif else_block:
                return exec_one(else_block, env)
        case FunDef(name, _, _) as f:
            scope = env[-1]
            scope[name] = f
        case Return(e):
            if e:
                return eval(e, env)
        case _:
            raise InterpretException("exec not implemented for " + str(statement))
    return None


def exec(statements: list[Stmt], env: Env) -> Value | None:
    for statement in statements:
        return_value = exec_one(statement, env)
        if return_value is not None:
            return return_value


if __name__ == "__main__":
    # Read file or use arg as program
    inp = sys.argv[1]
    try:
        with open(inp) as f:
            inp = f.read()
    except FileNotFoundError:
        pass

    # Parse and execute
    try:
        parser = ProgramParser(inp)
        program = parser.program()
        env: Env = [{}]
        exec(program, env)
    except ParseException as e:
        print(f"{e.message} at {e.line}:{e.column}")
    except InterpretException as e:
        print(e.message)
