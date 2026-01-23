import unittest
from program_parser import ProgramParser
from statement_parser import *


class ProgramParserTest(unittest.TestCase):
    def test_fun_decl(self):
        program = ProgramParser(
            "fun foo(x, y) { return add x y; } let x = call foo(1, 2);"
        ).parse_program()
        self.assertEqual(
            [
                FunctionDefinition(
                    "foo",
                    ["x", "y"],
                    Block(
                        [Return(BinaryOperation("add", Variable("x"), Variable("y")))]
                    ),
                ),
                VariableDefinition("x", FunctionCall("foo", [IntLit(1), IntLit(2)])),
            ],
            program,
        )


if __name__ == "__main__":
    unittest.main()
