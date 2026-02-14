from statement import *
from parser import debug_log

type Value = int


@dataclass
class InterpretError(Exception):
    message: str


@dataclass
class Interpreter:
    # Variables and their values
    env: dict[str, Value]
    # For storing return indices
    stack: list[int]
    # For storing label positions
    labels: dict[str, int]
    # For storing procedures
    procedures: dict[str, tuple[Proc, int]]
    # The statements of the program
    program: list[Statement]
    # The position in the program
    position: int

    def __init__(self, program: list[Statement]):
        # Initialize interpreter state
        self.program = program
        self.position = 0
        self.env = {}
        self.stack = []
        self.labels = {}
        self.procedures = {}
        # Pre-process the program to find all labels and procedures
        for position, statement in enumerate(self.program):
            match statement:
                case Label(name):
                    self.labels[name] = position
                case Proc(name, _) as proc:
                    self.procedures[name] = (proc, position)
                case _:
                    pass

    def __repr__(self):
        return f"Interpreter(pos={self.position}, env={self.env}, stack={self.stack}, labels={self.labels}, procs={self.procedures})"

    def execute_program(self):
        while self.position < len(self.program):
            statement = self.program[self.position]
            debug_log(f"interpreter.py | execute({statement}) in {self}")
            self.position += 1
            self.execute_statement(statement)

    def execute_statement(self, statement: Statement):
        match statement:
            case Skip():
                pass
            case Print(expr):
                print(self.eval_expr(expr))
            case Let(name, expr):
                evaluated_value = self.eval_expr(expr)
                self.env[name] = evaluated_value
            case Inc(left, right):
                self.env[left] = self.env[left] + self.eval_expr(right)
            case Dec(left, right):
                self.env[left] = self.env[left] - self.eval_expr(right)
            case Mul(left, right):
                self.env[left] = self.env[left] * self.eval_expr(right)
            case Swap(left, right):
                self.env[left], self.env[right] = self.env[right], self.env[left]
            case Label(_):
                # We don't need to do anything. Goto will find the label.
                pass
            case Goto(label):
                self.position = self.labels[label]
            case If(left, op, right, statement):
                l = self.eval_expr(left)
                r = self.eval_expr(right)
                apply = {
                    "==": l == r,
                    "<": l < r,
                    ">": l > r,
                    "<=": l <= r,
                    ">=": l >= r,
                    "!=": l != r,
                }
                if apply[op]:
                    self.execute_statement(statement)
            case Exit():
                self.position = len(self.program)
            case Proc(name, _):
                # Nothing to do. Goto will find it.
                pass
            case Call(name, args):
                self.stack.append(self.position)
                proc, position = self.procedures[name]
                self.position = position
                for p, a in zip(proc.params, args):
                    evaluated_value = self.eval_expr(a)
                    self.env[p] = evaluated_value
            case Return():
                self.position = self.stack.pop()

    def eval_expr(self, e: Expression) -> Value:
        if type(e) == int:
            return e
        elif type(e) == str:
            return self.env[e]
        raise TypeError(f"Invalid expression: {e}")


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Run booster-lang programs")
    parser.add_argument(
        "input", nargs="?", help="Input file or program string (default: stdin)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    import parser as parser_module

    parser_module.debug = args.debug

    if args.input is None:
        input_str = __import__("sys").stdin.read()
    elif os.path.isfile(args.input):
        with open(args.input, "r") as f:
            input_str = f.read()
    else:
        input_str = args.input

    from parser import parse_program, ParseError

    try:
        program = parse_program(input_str)
        interpreter = Interpreter(program)
        interpreter.execute_program()
    except ParseError as e:
        print(f"Parser error: {e.message}")
    except KeyError as e:
        print(f"Undefined variable: {e}")
