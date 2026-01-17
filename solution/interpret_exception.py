from dataclasses import dataclass


from dataclasses import dataclass


@dataclass
class InterpretException(Exception):
    message: str
