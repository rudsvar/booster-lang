from statement_parser import *
import sys


# Values that expressions are evaluated to.
type Value = int | str | bool | list[Value] | FunctionDefinition


# Exception for when interpreting fails, like when variables are not set
@dataclass
class InterpretException(Exception):
    message: str


# Environment and environment helper functions
type Env = list[dict[str, Value]]


def define_var(var: str, value: Value, env: Env):
    env[-1][var] = value


def lookup_var(var: str, env: Env) -> Value:
    """
    Look up a variable's value from the environment by iterating from the last to first scope.
    To check if a variable is in a scope, you can use `val = scope.get(var)` and return it if `val is not None`.
    """
    for scope in reversed(env):
        val = scope.get(var)
        if val is not None:
            return val
    raise InterpretException(f'Undefined variable "{var}"')


def assign_var(var: str, value: Value, env: Env):
    """
    Assign a new value to an existing variable.
    This is very similar to `lookup_var`, except we update the value in the scope we find the variable in.
    """
    for scope in reversed(env):
        if scope.get(var) is not None:
            scope[var] = value
            return
    raise InterpretException(f'Undefined variable "{var}"')


# Evaluation of expressions


def eval_int(i: int) -> Value:
    """
    An int cannot be simplified further and can just be returned.

    >>> eval_int(42)
    42
    """
    return i


def eval_string_literal(s: str) -> Value:
    """
    A string cannot be simplified further and can just be returned.

    >>> eval_string_literal("hello")
    'hello'
    """
    return s


def eval_bool(b: bool) -> Value:
    """
    A bool cannot be simplified further and can just be returned.

    >>> eval_bool(True)
    True
    """
    return b


def eval_var(var: Variable, env: Env) -> Value:
    """
    Look up the variable's name in the environment.

    >>> env: Env = [{"x": 42}]
    >>> eval_var(Variable(name="x"), env)
    42
    >>> env: Env = [{"x": 10}, {"y": 20}]
    >>> eval_var(Variable(name="y"), env)
    20
    >>> eval_var(Variable(name="x"), env)
    10
    """
    return lookup_var(var.name, env)


def eval_binary_operation(binop: BinaryOperation, env: Env) -> Value:
    """
    Evaluate the two operand expressions, and match on the operator to decide what to do.

    >>> env: Env = [{}]
    >>> eval_binary_operation(BinaryOperation(op="add", e1=2, e2=3), env)
    5
    """
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


def eval_list(list: list[Expression], env: Env) -> Value:
    """
    Evaluate each expression in the elements of the list.

    >>> env: Env = [{'x': 2}]
    >>> eval_list([1, Variable('x'), BinaryOperation('add', 1, 2)], env)
    [1, 2, 3]
    """
    return [eval_expr(e, env) for e in list]


def eval_function_call(function_call: FunctionCall, env: Env) -> Value | None:
    name = function_call.name
    args = function_call.args

    # Look up function in scope
    f = lookup_var(name, env)
    if type(f) != FunctionDefinition:
        raise InterpretException(f"{f} is not callable")

    # Optional: Check argument length matches parameter length
    params = f.params
    if len(params) != len(args):
        raise InterpretException(
            f"{name} expects {len(params)} arguments, but got {len(args)}"
        )

    # Optional: Create an environment that the function should run in. Alternatively just use env.
    # Mine includes a copy the top level scope to get global variables and functions and a fresh scope for parameter values.
    function_env: Env = [
        env[0],
        {},
    ]

    # Add parameters to environment
    for param, arg in zip(params, args):
        # Set parameter to evaluated argument
        arg_value = eval_expr(arg, env)
        define_var(param, arg_value, function_env)

    # Run body with function env
    return exec_statement(f.body, function_env)


def eval_expr(e: Expression, env: Env) -> Value:
    """
    Evaluates any kind of expression. Delegates to separate evaluator functions for each kind.

    >>> env: Env = [{}]
    >>> eval_expr(42, env)
    42
    >>> eval_expr("hello", env)
    'hello'
    >>> eval_expr(True, env)
    True
    >>> eval_expr([1, 2, 3], env)
    [1, 2, 3]
    >>> env: Env = [{"x": 10}]
    >>> eval_expr(Variable(name="x"), env)
    10
    >>> eval_expr(BinaryOperation(op="add", e1=5, e2=3), env)
    8
    >>> eval_expr(BinaryOperation(op="eq", e1=5, e2=5), env)
    True
    """
    match e:
        # bool must be first since it's a subclass of int
        case bool():
            return eval_bool(e)
        case int():
            return eval_int(e)
        case str():
            return eval_string_literal(e)
        case Variable():
            return eval_var(e, env)
        case list():
            return eval_list(e, env)
        case BinaryOperation():
            return eval_binary_operation(e, env)
        case FunctionCall() as f:
            return_value = eval_function_call(e, env)
            # Ensure the function returned a value
            if return_value is None:
                raise InterpretException(
                    f"Return value of {f.name} was None. It must return something."
                )
            return return_value
        case _:
            raise InterpretException("eval not implemented for " + str(e))


# Execution of statements


def exec_shout(print_stmt: Shout, env: Env):
    """
    Execute a `shout` statement by evaluating the expression and printing it in uppercase.

    >>> env: Env = [{}]
    >>> exec_shout(Shout(expr="hello"), env)
    HELLO
    """
    value = eval_expr(print_stmt.expr, env)
    print(str(value).upper())


def exec_var_def(var_def: VariableDefinition, env: Env):
    """
    Execute a variable definition by evaluating the expression and storing it in the environment.

    >>> env: Env = [{}]
    >>> exec_var_def(VariableDefinition(var_name="x", expr=42), env)
    >>> env
    [{'x': 42}]
    """
    value = eval_expr(var_def.expr, env)
    define_var(var_def.var_name, value, env)


def exec_assignment(assignment: Assignment, env: Env):
    """
    Execute an assignment by evaluating the expression and assigning it to an existing variable.

    >>> env: Env = [{"x": 10}]
    >>> exec_assignment(Assignment(var_name="x", expr=20), env)
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
    >>> exec_if(If(condition=True, then_block=Block(statements=[]), else_block=None), env)
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
    >>> body = Block(statements=[Assignment(var_name="x", expr=BinaryOperation(op="sub", e1=Variable(name="x"), e2=1))])
    >>> loop = Whilst(condition=BinaryOperation(op="neq", e1=Variable(name="x"), e2=0), body=body)
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
    >>> exec_return(Return(expr=42), env)
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
    >>> exec_statement(VariableDefinition(var_name="x", expr=42), env)
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
    >>> program = [VariableDefinition(var_name="x", expr=10), VariableDefinition(var_name="y", expr=20)]
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

    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file_or_code>")
        sys.exit(1)

    try:
        from program_parser import ProgramParser

        code = read_input(sys.argv[1])
        parser = ProgramParser(code)
        program = parser.parse_program()
        env: Env = [{}]
        exec_program(program, env)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
    except InterpretException as e:
        print("error:", e.message)
        sys.exit(1)
