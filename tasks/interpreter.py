from env import Env
from interpret_exception import InterpretException
from value import Value
from statement_parser import *


def eval_int(i: Int) -> Value:
    raise NotImplementedError("TODO")


def eval_str_lit(s: StrLit) -> Value:
    raise NotImplementedError("TODO")


def eval_bool(b: Bool) -> Value:
    raise NotImplementedError("TODO")


def eval_var(var: Var, env: Env) -> Value:
    raise NotImplementedError("TODO")


def eval_list(list: List, env: Env) -> Value:
    raise NotImplementedError("TODO")


def eval_binop(binop: BinOp, env: Env) -> Value:
    raise NotImplementedError("TODO")


def eval_function_call(function_call: FunCall, env: Env) -> Value | None:
    raise NotImplementedError("TODO")


def eval_expr(e: Expr, env: Env) -> Value:
    """Evaluates any kind of expression. Delegates to separate evaluator functions for each kind."""
    raise NotImplementedError("TODO")


def exec_var_def(var_def: VarDef, env: Env):
    raise NotImplementedError("TODO")


def exec_assignment(assignment: Assignment, env: Env):
    raise NotImplementedError("TODO")


def exec_print(print_stmt: Shout, env: Env):
    raise NotImplementedError("TODO")


def exec_block(block: Block, env: Env) -> Value | None:
    raise NotImplementedError("TODO")


def exec_if(if_stmt: If, env: Env) -> Value | None:
    raise NotImplementedError("TODO")


def exec_whilst(whilst_stmt: Whilst, env: Env):
    raise NotImplementedError("TODO")


def exec_fun_def(fun_def: FunDef, env: Env):
    raise NotImplementedError("TODO")


def exec_return(return_stmt: Return, env: Env) -> Value | None:
    raise NotImplementedError("TODO")


def exec_statement(statement: Stmt, env: Env) -> Value | None:
    """Executes any kind of statement. Delegates to separate executor functions for each kind."""
    raise NotImplementedError("TODO")


def exec_program(program: list[Stmt], env: Env) -> Value | None:
    raise NotImplementedError("TODO")
