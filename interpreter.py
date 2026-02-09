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

    def run(self):
        while self.position < len(self.program):
            statement = self.program[self.position]
            debug_log(f"interpreter.py | execute({statement}) in {self}")
            self.position += 1
            self.execute(statement)

    def execute(self, statement: Statement):
        match statement:
            case Skip():
                # Do nothing
                pass
            case Print(value):
                print(self.eval(value))
            case VarDef(name, value):
                self.var_def(name, value)
            case Inc(left, right):
                self.inc(left, right)
            case Dec(left, right):
                self.dec(left, right)
            case Mul(left, right):
                self.mul(left, right)
            case Swap(left, right):
                self.swap(left, right)
            case Label(_):
                # We don't need to do anything. Goto will find the label.
                pass
            case Goto(label):
                self.goto(label)
            case If(left, op, right, statement):
                self.exec_if(left, op, right, statement)
            case Exit():
                self.position = len(self.program)
            case Proc(name, _):
                # Nothing to do. Goto will find it.
                pass
            case Call(name, args):
                self.call(name, args)
            case Return():
                self.ret()

    def eval(self, e: Expression) -> Value:
        if type(e) == int:
            return e
        elif type(e) == str:
            return self.env[e]
        raise TypeError(f"Invalid expression: {e}")

    def print(self, value: Expression):
        print(self.eval(value))

    def var_def(self, name: str, value: Expression):
        evaluated_value = self.eval(value)
        self.env[name] = evaluated_value

    def inc(self, var: str, addend: Expression):
        self.env[var] = self.env[var] + self.eval(addend)

    def dec(self, var: str, subtrahend: Expression):
        self.env[var] = self.env[var] - self.eval(subtrahend)

    def mul(self, var: str, multiplier: Expression):
        self.env[var] = self.env[var] * self.eval(multiplier)

    def swap(self, left: str, right: str):
        self.env[left], self.env[right] = self.env[right], self.env[left]

    def goto(self, label: str):
        self.position = self.labels[label]

    def exec_if(
        self, left: Expression, op: str, right: Expression, statement: Statement
    ):
        l = self.eval(left)
        r = self.eval(right)
        apply = {
            "==": l == r,
            "<": l < r,
            ">": l > r,
            "<=": l <= r,
            ">=": l >= r,
            "!=": l != r,
        }
        if apply[op]:
            self.execute(statement)

    def call(self, name: str, args: list[Expression]):
        self.stack.append(self.position)
        proc, position = self.procedures[name]
        self.position = position
        for p, a in zip(proc.params, args):
            a = self.eval(a)
            self.var_def(p, a)

    def ret(self):
        self.position = self.stack.pop()


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
        interpreter.run()
    except ParseError as e:
        print(f"Parser error: {e.message}")
    except KeyError as e:
        print(f"Undefined variable: {e}")
