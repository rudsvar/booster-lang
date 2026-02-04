from dataclasses import dataclass
from typing import Any

type Statement = Set | Print | Push | Pop | Sub | Add | Label | Jmp | Jeq | Jlt | Fun | Call | Return


@dataclass
class Set:
    name: str
    value: Any


@dataclass
class Print:
    value: Any


@dataclass
class Push:
    value: Any


@dataclass
class Pop:
    name: str


@dataclass
class Sub:
    left: str
    right: Any


@dataclass
class Add:
    left: str
    right: Any


@dataclass
class Label:
    name: str


@dataclass
class Jmp:
    label: str


@dataclass
class Jeq:
    left: Any
    right: Any
    label: str


@dataclass
class Jlt:
    left: Any
    right: Any
    label: str


@dataclass
class Fun:
    name: str
    params: list[str]


@dataclass
class Call:
    name: str
    args: list[Any]


@dataclass
class Return:
    name: str
    value: Any


class Interpreter:
    statements: list[Statement]
    position: int = 0
    env: dict[str, Any] = {}
    stack: list[Any] = []

    def __init__(self, statements):
        self.statements = statements

    def run(self):
        while self.position < len(self.statements):
            self.step()

    def step(self):
        statement = self.statements[self.position]
        print(
            f"\033[2;30m{self.position} {statement} | {self.env} | {self.stack}\033[0m"
        )
        self.position += 1
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


if __name__ == "__main__":
    i = Interpreter(
        [
            Call("foo", [3]),
            Fun("foo", ["n"]),
            Print("n"),
            Jeq("n", 0, "exit"),
            Sub("n", 1),
            Call("foo", ["n"]),
            Label("exit"),
        ]
    )
    i.run()
