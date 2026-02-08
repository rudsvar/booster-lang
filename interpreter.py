from typing import Any
from statement import *
from parser import debug_log


class Interpreter:
    statements: list[Statement]

    def __init__(self, statements):
        self.statements = statements
        self.position: int = 0
        self.env: dict[str, Any] = {}
        self.stack: list[Any] = []

    def run(self):
        while self.position < len(self.statements):
            statement = self.statements[self.position]
            debug_log(f"{self.position} {statement} | {self.env} | {self.stack}")
            self.position += 1
            self.execute(statement)

    def execute(self, statement):
        match statement:
            case Skip():
                # Do nothing
                pass
            case Print(value):
                print(self.eval(value))
                self.print(value)
            case VarDef(name, value):
                self.var_def(name, value)
            case Inc(left, right):
                self.inc(left, right)
            case Dec(left, right):
                self.sub(left, right)
            case Label(_):
                # We don't need to do anything. Goto will find the label.
                pass
            case Goto(label):
                self.goto(label)
            case If(left, op, right, statement):
                self.exec_if(left, op, right, statement)
            case Fun(name, params):
                self.fun(name, params)
            case Call(name, args):
                self.call(name, args)
            case Return(name, value):
                self.return_(name, value)
            case Halt():
                self.position = len(self.statements)

    def eval(self, value: Expression) -> int:
        print(type(value))
        match value:
            case str():
                return self.env[value]
            case int():
                return value
        raise TypeError("Value has invalid type")

    def var_def(self, name: str, value: Any):
        self.env[name] = self.eval(value)

    def print(self, value: Any):
        print(self.eval(value))

    def push(self, value: Any):
        self.stack.append(self.eval(value))

    def pop(self, name: str):
        value = self.stack.pop()
        self.env[name] = value

    def sub(self, left: str, right: Any):
        self.env[left] = self.eval(self.env[left]) - self.eval(right)

    def inc(self, left: str, right: Any):
        self.env[left] = self.eval(self.env[left]) + self.eval(right)

    def goto(self, label: str):
        for position, statement in enumerate(self.statements):
            match statement:
                case Label(l) if l == label:
                    self.position = position
                    break
                case Fun(name, _) if name == label:
                    self.position = position
                    break
                case _:
                    pass

    def fun(self, _: str, params: list[str]):
        for param in reversed(params):
            self.pop(param)

    def call(self, name: str, args: list[Any]):
        self.push(str(self.position))  # Return addr
        for arg in args:
            self.push(arg)
        self.goto(name)

    def return_(self, name: str, value: Any):
        self.position = int(self.stack.pop())

    def exec_if(
        self, left: Expression, op: str, right: Expression, statement: Statement
    ):
        l = self.eval(left)
        r = self.eval(right)
        apply = {"==": l == r, "<": l < r, ">": l > r}
        if apply[op]:
            self.execute(statement)


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

    from parser import parse_program
    from pprint import pprint

    program = parse_program(input_str)
    pprint(program)
    interpreter = Interpreter(program)
    interpreter.run()
