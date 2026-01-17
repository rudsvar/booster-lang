import unittest
from solution.parser.program import ProgramParser
from solution.parser.statement import *


class ProgramParserTest(unittest.TestCase):
    def test_fun_decl(self):
        program = ProgramParser(
            "fun foo(x, y) { return add x y; } let x = call foo(1, 2);"
        ).parse_program()
        self.assertEqual(
            [
                FunDef(
                    "foo",
                    ["x", "y"],
                    Block([Return(BinOp("add", Var("x"), Var("y")))]),
                ),
                VarDef("x", FunCall("foo", [Int(1), Int(2)])),
            ],
            program,
        )


if __name__ == "__main__":
    unittest.main()
