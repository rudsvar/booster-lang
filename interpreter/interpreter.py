from dataclasses import dataclass
from parser.program import *
import sys


"""Values that expressions can be evaluated to"""
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

    def define_var(self, var: str, value: Value):
        """Define a new variable in the nearest scope"""
        inner_scope = self.inner_scope()
        inner_scope[var] = value

    def lookup_var(self, var: str) -> Value:
        """Look up a variable's value from the environment"""
        for scope in reversed(self.scopes):
            val = scope.get(var)
            if val is not None:
                return val
        raise InterpretException(f'Undefined variable "{var}"')

    def assign_var(self, var: str, value: Value):
        """Assign a new value to an existing variable"""
        for scope in reversed(self.scopes):
            if scope.get(var) is not None:
                scope[var] = value
                return
        raise InterpretException(f'Undefined variable "{var}"')


@dataclass
class Interpreter:

    def eval_int(self, i: Int):
        return i.value

    def eval_str_lit(self, s: StrLit):
        return s.value

    def eval_bool(self, b: Bool):
        return b.value

    def eval_var(self, var: Var, env: Env):
        return env.lookup_var(var.name)

    def eval_list(self, list: List, env: Env):
        return [self.eval_expr(e, env) for e in list.elements]

    def eval_binop(self, binop: BinOp, env: Env):
        operator = binop.op
        v1 = self.eval_expr(binop.e1, env)
        v2 = self.eval_expr(binop.e2, env)
        match operator:
            case "+" if type(v1) == int and type(v2) == int:
                return v1 + v2
            case "-" if type(v1) == int and type(v2) == int:
                return v1 - v2
            case "==" if type(v1) == type(v2):
                return v1 == v2
            case _:
                raise InterpretException(
                    f"Operator {operator} does not work on {v1} and {v2}"
                )

    def eval_function_call(self, function_call: FunCall, env: Env) -> Value | None:
        name = function_call.name
        args = function_call.args
        # Look up function in scope
        f = env.lookup_var(name)
        if type(f) != FunDef:
            raise InterpretException(f"{f} is not callable")

        # Check argument length matches parameter length
        params = f.params
        if len(params) != len(args):
            raise InterpretException(
                f"{name} expects {len(params)} arguments, but got {len(args)}"
            )

        # Create the environment that the function should run in
        function_env: Env = Env()  # Start by creating an empty one
        function_env.scopes = [
            env.top_level_scope()
        ]  # Copy the top level scope to get global variables and functions
        function_env.open_scope()  # Open a new scope to bind arguments to parameters
        for param, arg in zip(params, args):
            # Evaluate argument and bind to parameter
            arg_value = self.eval_expr(arg, env)
            function_env.define_var(param, arg_value)

        # Run body with function env
        return self.exec_statement(f.body, function_env)

    def eval_expr(self, e: Expr, env: Env) -> Value:
        match e:
            case Int():
                return self.eval_int(e)
            case StrLit():
                return self.eval_str_lit(e)
            case Bool():
                return self.eval_bool(e)
            case Var():
                return self.eval_var(e, env)
            case List():
                return self.eval_list(e, env)
            case BinOp():
                return self.eval_binop(e, env)
            case FunCall():
                return self.eval_function_call(e, env)
            case _:
                raise InterpretException("eval not implemented for " + str(e))

    def exec_var_def(self, var_def: VarDef, env: Env):
        value = self.eval_expr(var_def.expr, env)
        env.define_var(var_def.var_name, value)

    def exec_assignment(self, assignment: Assignment, env: Env):
        value = self.eval_expr(assignment.expr, env)
        env.assign_var(assignment.var_name, value)

    def exec_print(self, print_stmt: Shout, env: Env):
        value = self.eval_expr(print_stmt.expr, env)
        print(str(value).upper())

    def exec_block(self, block: Block, env: Env) -> Value | None:
        env.open_scope()
        return_value = self.exec_program(block.statements, env)
        env.close_scope()
        return return_value

    def exec_if(self, if_stmt: If, env: Env) -> Value | None:
        condition = self.eval_expr(if_stmt.condition, env)
        if condition:
            return self.exec_statement(if_stmt.then_block, env)
        elif if_stmt.else_block:
            return self.exec_statement(if_stmt.else_block, env)

    def exec_fun_def(self, fun_def: FunDef, env: Env):
        env.define_var(fun_def.name, fun_def)

    def exec_return(self, return_stmt: Return, env: Env) -> Value | None:
        if return_stmt.expr:
            return self.eval_expr(return_stmt.expr, env)
        return None

    def exec_statement(self, statement: Stmt, env: Env) -> Value | None:
        match statement:
            case VarDef():
                return self.exec_var_def(statement, env)
            case Assignment():
                return self.exec_assignment(statement, env)
            case Shout():
                return self.exec_print(statement, env)
            case Block():
                return self.exec_block(statement, env)
            case If():
                return self.exec_if(statement, env)
            case FunDef():
                return self.exec_fun_def(statement, env)
            case Return():
                return self.exec_return(statement, env)
            case _:
                raise InterpretException("exec not implemented for " + str(statement))

    def exec_program(self, program: list[Stmt], env: Env) -> Value | None:
        for statement in program:
            return_value = self.exec_statement(statement, env)
            if return_value is not None:
                return return_value

    def exec_string(self, input: str, env: Env) -> Value | None:
        """Parses and interprets text"""
        parser = ProgramParser(input)
        program = parser.program()
        self.exec_program(program, env)

    def exec_file(self, path: str, env: Env) -> Value | None:
        """Reads, parses and interprets a file"""
        with open(path) as f:
            inp = f.read()
            self.exec_string(inp, env)


if __name__ == "__main__":
    interpreter = Interpreter()
    env = Env()
    # Read file or use arg as program
    input = sys.argv[1]
    try:
        interpreter.exec_file(input, env)
    except FileNotFoundError:
        pass

    # Parse and execute
    try:
        interpreter.exec_string(input, env)
    except ParseException as e:
        print(f"{e.message} at {e.line}:{e.column}")
    except InterpretException as e:
        print(e.message)
