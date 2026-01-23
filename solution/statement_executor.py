from statement_parser import *
from expression_evaluator import *
import sys


def exec_shout(print_stmt: Shout, env: Env):
    """
    Execute a `shout` statement by evaluating the expression and printing it in uppercase.

    >>> env: Env = [{}]
    >>> exec_shout(Shout(expr=StrLit(value="hello")), env)
    HELLO
    """
    value = eval_expr(print_stmt.expr, env)
    print(str(value).upper())


def exec_var_def(var_def: VariableDefinition, env: Env):
    """
    Execute a variable definition by evaluating the expression and storing it in the environment.

    >>> env: Env = [{}]
    >>> exec_var_def(VariableDefinition(var_name="x", expr=IntLit(value=42)), env)
    >>> env
    [{'x': 42}]
    """
    value = eval_expr(var_def.expr, env)
    define_var(var_def.var_name, value, env)


def exec_assignment(assignment: Assignment, env: Env):
    """
    Execute an assignment by evaluating the expression and assigning it to an existing variable.

    >>> env: Env = [{"x": 10}]
    >>> exec_assignment(Assignment(var_name="x", expr=IntLit(value=20)), env)
    >>> env
    [{'x': 20}]
    """
    value = eval_expr(assignment.expr, env)
    assign_var(assignment.var_name, value, env)


def exec_block(block: Block, env: Env) -> Value | None:
    """
    Execute a block by creating a new scope, executing statements, and then closing the scope.

    >>> env: Env = [{"x": 10}]
    >>> exec_block(Block(statements=[]), env)
    >>> env
    [{'x': 10}]
    """
    env.append({})
    return_value = exec_program(block.statements, env)
    env.pop()
    return return_value


def exec_if(if_stmt: If, env: Env) -> Value | None:
    """
    Execute an if statement by evaluating the condition and executing the appropriate branch.

    >>> env: Env = [{}]
    >>> exec_if(If(condition=BoolLit(value=True), then_block=Block(statements=[]), else_block=None), env)
    """
    condition = eval_expr(if_stmt.condition, env)
    if condition:
        return exec_statement(if_stmt.then_block, env)
    elif if_stmt.else_block:
        return exec_statement(if_stmt.else_block, env)


def exec_whilst(whilst_stmt: Whilst, env: Env):
    """
    Execute a while loop by repeatedly evaluating the condition and executing the body.
    The condition is re-evaluated after each iteration.

    >>> env: Env = [{"x": 2}]
    >>> body = Block(statements=[Assignment(var_name="x", expr=BinaryOperation(op="sub", e1=Variable(name="x"), e2=IntLit(value=1)))])
    >>> loop = Whilst(condition=BinaryOperation(op="neq", e1=Variable(name="x"), e2=IntLit(value=0)), body=body)
    >>> exec_whilst(loop, env)
    >>> env
    [{'x': 0}]
    """
    condition = eval_expr(whilst_stmt.condition, env)
    while condition:
        # Run the whilst body. The body should update variables in the condition to avoid an infinite loop
        exec_statement(whilst_stmt.body, env)
        # We must evaluate the condition again with the updated environment
        condition = eval_expr(whilst_stmt.condition, env)


def exec_function_definition(fun_def: FunctionDefinition, env: Env):
    """
    Execute a function definition by storing the function in the environment.

    >>> env: Env = [{}]
    >>> fun = FunctionDefinition(name="add", params=["x", "y"], body=Block(statements=[]))
    >>> exec_function_definition(fun, env)
    >>> env
    [{'add': FunctionDefinition(name='add', params=['x', 'y'], body=Block(statements=[]))}]
    """
    define_var(fun_def.name, fun_def, env)


def exec_return(return_stmt: Return, env: Env) -> Value | None:
    """
    Execute a return statement by evaluating the expression and returning its value.
    If no expression is provided, returns None.

    >>> env: Env = [{}]
    >>> exec_return(Return(expr=IntLit(value=42)), env)
    42
    >>> exec_return(Return(expr=None), env)
    """
    if return_stmt.expr is not None:
        return eval_expr(return_stmt.expr, env)
    return None


def exec_statement(statement: Statement, env: Env) -> Value | None:
    """
    Executes any kind of statement. Delegates to separate executor functions for each kind.

    >>> env: Env = [{}]
    >>> exec_statement(VariableDefinition(var_name="x", expr=IntLit(value=42)), env)
    >>> env
    [{'x': 42}]
    """
    match statement:
        case VariableDefinition():
            return exec_var_def(statement, env)
        case Assignment():
            return exec_assignment(statement, env)
        case Shout():
            return exec_shout(statement, env)
        case Block():
            return exec_block(statement, env)
        case If():
            return exec_if(statement, env)
        case Whilst():
            return exec_whilst(statement, env)
        case FunctionDefinition():
            return exec_function_definition(statement, env)
        case Return():
            return exec_return(statement, env)
        case _:
            raise InterpretException("exec not implemented for " + str(statement))


def exec_program(program: list[Statement], env: Env) -> Value | None:
    """
    Execute a list of statements in order, returning the value of the first statement that returns a value.

    >>> env: Env = [{}]
    >>> program = [VariableDefinition(var_name="x", expr=IntLit(value=10)), VariableDefinition(var_name="y", expr=IntLit(value=20))]
    >>> exec_program(program, env)
    >>> env
    [{'x': 10, 'y': 20}]
    """
    for statement in program:
        return_value = exec_statement(statement, env)
        if return_value is not None:
            return return_value


if __name__ == "__main__":

    def read_input(input_path: str) -> str:
        """Try to read file, otherwise treat input as code string"""
        try:
            with open(input_path) as f:
                return f.read()
        except FileNotFoundError:
            return input_path

    if len(sys.argv) != 2:
        print("Usage: python statement_executor.py <statement>")
        sys.exit(1)

    try:
        code = read_input(sys.argv[1])
        parser = StatementParser(code)
        stmt = parser.parse_statement()
        if parser.input.strip():
            parser.fail("Only expected a single statement")
        env: Env = [{}]
        exec_statement(stmt, env)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
    except InterpretException as e:
        print("error:", e.message)
        sys.exit(1)
