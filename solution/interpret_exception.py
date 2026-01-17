from dataclasses import dataclass


@dataclass
class InterpretException(Exception):
    message: str
