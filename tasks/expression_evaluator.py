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


def eval_int(i: IntLit) -> Value:
    """
    An int cannot be simplified further and can just be returned.

    >>> eval_int(IntLit(42))
    42
    """
    raise NotImplementedError("eval_int is not implemented")


def eval_string_literal(s: StrLit) -> Value:
    """
    A string cannot be simplified further and can just be returned.

    >>> eval_string_literal(StrLit("hello"))
    'hello'
    """
    raise NotImplementedError("eval_string_literal is not implemented")


def eval_bool(b: BoolLit) -> Value:
    """
    A bool cannot be simplified further and can just be returned.

    >>> eval_bool(BoolLit(True))
    True
    """
    raise NotImplementedError("eval_bool is not implemented")


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
    raise NotImplementedError("eval_var is not implemented")


def eval_binary_operation(binop: BinaryOperation, env: Env) -> Value:
    """
    Evaluate the two operand expressions, and match on the operator to decide what to do.

    >>> env: Env = [{}]
    >>> eval_binary_operation(BinaryOperation(op="add", e1=IntLit(2), e2=IntLit(3)), env)
    5
    """
    raise NotImplementedError("eval_binary_operation is not implemented")


def eval_list(lst: ListLit, env: Env) -> Value:
    """
    Evaluate each expression in the elements of the list.

    >>> env: Env = [{'x': 2}]
    >>> eval_list(ListLit([IntLit(1), Variable('x'), BinaryOperation('add', IntLit(1), IntLit(2))]), env)
    [1, 2, 3]
    """
    raise NotImplementedError("eval_list is not implemented")


def eval_function_call(function_call: FunctionCall, env: Env) -> Value | None:
    raise NotImplementedError("eval_function_call is not implemented")


def eval_expr(e: Expression, env: Env) -> Value:
    """
    Evaluates any kind of expression. Delegates to separate evaluator functions for each kind.

    >>> env: Env = [{}]
    >>> eval_expr(IntLit(42), env)
    42
    >>> eval_expr(StrLit("hello"), env)
    'hello'
    >>> eval_expr(BoolLit(True), env)
    True
    >>> eval_expr(ListLit([IntLit(1), IntLit(2), IntLit(3)]), env)
    [1, 2, 3]
    >>> env: Env = [{"x": 10}]
    >>> eval_expr(Variable(name="x"), env)
    10
    >>> eval_expr(BinaryOperation(op="add", e1=IntLit(5), e2=IntLit(3)), env)
    8
    >>> eval_expr(BinaryOperation(op="eq", e1=IntLit(5), e2=IntLit(5)), env)
    True
    """
    match e:
        case IntLit():
            return eval_int(e)
        case BoolLit():
            return eval_bool(e)
        case StrLit():
            return eval_string_literal(e)
        case ListLit():
            return eval_list(e, env)
        case Variable():
            return eval_var(e, env)
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
