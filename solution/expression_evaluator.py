from expression_parser import *
import sys

from statement_parser import FunctionDefinition


# Values that expressions are evaluated to.
type Value = int | str | bool | list[Value] | FunctionDefinition


# Exception for when interpreting fails, like when variables are not set
@dataclass
class InterpretException(Exception):
    message: str


# Environment and environment helper functions
type Env = list[dict[str, Value]]


def define_var(var: str, value: Value, env: Env):
    """Add a variable to the innermost (last added) scope."""
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
        case "add" if type(v1) == str and type(v2) == str:
            return v1 + v2
        case "add" if type(v1) == list and type(v2) == list:
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
    # Import here to avoid circular dependency
    from statement_executor import exec_statement

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


if __name__ == "__main__":

    def read_input(input_path: str) -> str:
        """Try to read file, otherwise treat input as code string"""
        try:
            with open(input_path) as f:
                return f.read()
        except FileNotFoundError:
            return input_path

    if len(sys.argv) != 2:
        print("Usage: python expression_evaluator.py <expression>")
        sys.exit(1)

    try:
        code = read_input(sys.argv[1])
        parser = ExpressionParser(code)
        expr = parser.parse_expr()
        env: Env = [{}]
        result = eval_expr(expr, env)
        print(result)
    except ParseException as e:
        print(f"error: {e.message} at {e.line}:{e.column}")
        sys.exit(1)
    except InterpretException as e:
        print("error:", e.message)
        sys.exit(1)
