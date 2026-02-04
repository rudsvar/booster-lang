from typing import Any
from statement import *
from parser import debug_log


class Interpreter:
    statements: list[Statement]
    position: int = 0
    env: dict[str, Any] = {}
    stack: list[Any] = []

    def __init__(self, statements):
        self.statements = statements

    def run(self):
        while self.position < len(self.statements):
            statement = self.statements[self.position]
            debug_log(f"{self.position} {statement} | {self.env} | {self.stack}")
            self.position += 1
            self.execute(statement)

    def execute(self, statement):
        match statement:
            case Set(name, value):
                self.set(name, value)
            case Print(value):
                self.print(value)
            case Push(value):
                self.push(value)
            case Pop(value):
                self.pop(value)
            case Sub(left, right):
                self.sub(left, right)
            case Add(left, right):
                self.add(left, right)
            case Jmp(label):
                self.jmp(label)
            case Jeq(left, right, label):
                self.jeq(left, right, label)
            case Jlt(left, right, label):
                self.jlt(left, right, label)
            case Fun(name, params):
                self.fun(name, params)
            case Call(name, args):
                self.call(name, args)
            case Return(name, value):
                self.return_(name, value)
            case If(left, op, right, statement):
                self.exec_if(left, op, right, statement)

    def evaluate_value(self, value: Value) -> int:
        match value:
            case str():
                return self.env[value]
            case int():
                return value
        raise TypeError("Value has invalid type")

    def set(self, name: str, value: Any):
        if type(value) == str:
            value = self.env[value]
        self.env[name] = value

    def print(self, value: Any):
        if type(value) == str:
            print(self.env[value])
        else:
            print(value)

    def push(self, value: Any):
        if type(value) == str:
            value = self.env[value]
        self.stack.append(value)

    def pop(self, name: str):
        value = self.stack.pop()
        self.env[name] = value

    def sub(self, left: str, right: Any):
        right = self.env.get(right) or right
        if type(right) == int:
            self.env[left] = int(self.env[left]) - right

    def add(self, left: str, right: Any):
        right = self.env.get(right) or right
        if type(right) == int:
            self.env[left] = int(self.env[left]) + right

    def jmp(self, label: str):
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

    def jeq(self, left: Any, right: Any, label: str):
        l = self.env.get(left) or left
        r = self.env.get(right) or right
        if l == r:
            self.jmp(label)

    def jlt(self, left: Any, right: Any, label: str):
        l = self.env.get(left) or left
        r = self.env.get(right) or right
        if l < r:
            self.jmp(label)

    def fun(self, _: str, params: list[str]):
        for param in reversed(params):
            self.pop(param)

    def call(self, name: str, args: list[Any]):
        self.push(str(self.position))  # Return addr
        for arg in args:
            self.push(arg)
        self.jmp(name)

    def return_(self, name: str, value: Any):
        self.position = int(self.stack.pop())

    def exec_if(self, left: Value, op: str, right: Value, statement: Statement):
        l = self.evaluate_value(left)
        r = self.evaluate_value(right)
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

    program = parse_program(input_str)
    print(program)
    interpreter = Interpreter(program)
    interpreter.run()
