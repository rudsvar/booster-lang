from statement import *
from parser import debug_log


class Interpreter:
    statements: list[Statement]

    def __init__(self, statements):
        self.statements = statements
        self.position: int = 0
        self.env: dict[str, int] = {}
        self.stack: list[int] = []

    def run(self):
        while self.position < len(self.statements):
            statement = self.statements[self.position]
            debug_log(
                f"Exec {statement} pos={self.position} env={self.env} stack={self.stack}"
            )
            self.position += 1
            self.execute(statement)

    def execute(self, statement):
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
                self.position = len(self.statements)
            case Fun(name, _):
                # Nothing to do. Goto will find it.
                pass
            case Call(name, args):
                self.call(name, args)
            case Return():
                self.ret()

    def eval(self, e: Expression) -> int:
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
        for position, statement in enumerate(self.statements):
            match statement:
                case Label(l) if l == label:
                    self.position = position
                    break

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
        # Store return position
        self.stack.append(self.position)
        # Find the function we're calling
        for position, statement in enumerate(self.statements):
            match statement:
                case Fun(name, params) if name:
                    # Go to function position
                    self.position = position
                    # Bind args to params
                    for p, a in zip(params, args):
                        a = self.eval(a)
                        self.var_def(p, a)
                    break

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

    parser_module.DEBUG = args.debug

    if args.input is None:
        input_str = __import__("sys").stdin.read()
    elif os.path.isfile(args.input):
        with open(args.input, "r") as f:
            input_str = f.read()
    else:
        input_str = args.input

    from parser import parse_program, ParseError
    from pprint import pprint

    try:
        program = parse_program(input_str)
        interpreter = Interpreter(program)
        interpreter.run()
    except ParseError as e:
        print(f"Parse error: {e.message}", file=__import__("sys").stderr)
        __import__("sys").exit(1)
