from env import Env
from interpret_exception import InterpretException
from value import Value
from statement_parser import *


# Evaluation of expressions


def eval_int(i: int) -> Value:
    return i


def eval_str_lit(s: str) -> Value:
    return s


def eval_bool(b: bool) -> Value:
    return b


def eval_var(var: Var, env: Env) -> Value:
    return env.lookup_var(var.name)


def eval_list(list: List, env: Env) -> Value:
    return [eval_expr(e, env) for e in list.elements]


def eval_binop(binop: BinOp, env: Env) -> Value:
    operator = binop.op
    v1 = eval_expr(binop.e1, env)
    v2 = eval_expr(binop.e2, env)
    match operator:
        case "add" if type(v1) == int and type(v2) == int:
            return v1 + v2
        case "sub" if type(v1) == int and type(v2) == int:
            return v1 - v2
        case "mul" if type(v1) == int and type(v2) == int:
            return v1 * v2
        case "div" if type(v1) == int and type(v2) == int:
            return v1 // v2
        case "eq" if type(v1) == type(v2):
            return v1 == v2
        case "neq" if type(v1) == type(v2):
            return v1 != v2
        case _:
            raise InterpretException(
                f"Operator {operator} does not support {v1} and {v2}"
            )


def eval_function_call(function_call: FunCall, env: Env) -> Value | None:
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
        arg_value = eval_expr(arg, env)
        function_env.define_var(param, arg_value)

    # Run body with function env
    return exec_statement(f.body, function_env)


def eval_expr(e: Expr, env: Env) -> Value:
    """Evaluates any kind of expression. Delegates to separate evaluator functions for each kind."""
    match e:
        # bool must be first since it's a subclass of int
        case bool():
            return eval_bool(e)
        case int():
            return eval_int(e)
        case str():
            return eval_str_lit(e)
        case Var():
            return eval_var(e, env)
        case List():
            return eval_list(e, env)
        case BinOp():
            return eval_binop(e, env)
        case FunCall():
            return eval_function_call(e, env)
        case _:
            raise InterpretException("eval not implemented for " + str(e))


# Execution of statements


def exec_var_def(var_def: VarDef, env: Env):
    value = eval_expr(var_def.expr, env)
    env.define_var(var_def.var_name, value)


def exec_assignment(assignment: Assignment, env: Env):
    value = eval_expr(assignment.expr, env)
    env.assign_var(assignment.var_name, value)


def exec_print(print_stmt: Shout, env: Env):
    value = eval_expr(print_stmt.expr, env)
    print(str(value).upper())


def exec_block(block: Block, env: Env) -> Value | None:
    env.open_scope()
    return_value = exec_program(block.statements, env)
    env.close_scope()
    return return_value


def exec_if(if_stmt: If, env: Env) -> Value | None:
    condition = eval_expr(if_stmt.condition, env)
    if condition:
        return exec_statement(if_stmt.then_block, env)
    elif if_stmt.else_block:
        return exec_statement(if_stmt.else_block, env)


def exec_whilst(whilst_stmt: Whilst, env: Env):
    condition = eval_expr(whilst_stmt.condition, env)
    while condition:
        # Run the whilst body. The body should update variables in the condition to avoid an infinite loop
        exec_statement(whilst_stmt.body, env)
        # We must evaluate the condition again with the updated environment
        condition = eval_expr(whilst_stmt.condition, env)


def exec_fun_def(fun_def: FunDef, env: Env):
    env.define_var(fun_def.name, fun_def)


def exec_return(return_stmt: Return, env: Env) -> Value | None:
    if return_stmt.expr is not None:
        return eval_expr(return_stmt.expr, env)
    return None


def exec_statement(statement: Stmt, env: Env) -> Value | None:
    """Executes any kind of statement. Delegates to separate executor functions for each kind."""
    match statement:
        case VarDef():
            return exec_var_def(statement, env)
        case Assignment():
            return exec_assignment(statement, env)
        case Shout():
            return exec_print(statement, env)
        case Block():
            return exec_block(statement, env)
        case If():
            return exec_if(statement, env)
        case Whilst():
            return exec_whilst(statement, env)
        case FunDef():
            return exec_fun_def(statement, env)
        case Return():
            return exec_return(statement, env)
        case _:
            raise InterpretException("exec not implemented for " + str(statement))


def exec_program(program: list[Stmt], env: Env) -> Value | None:
    for statement in program:
        # If a statement returns something, propagate that upwards
        return_value = exec_statement(statement, env)
        if return_value is not None:
            return return_value
