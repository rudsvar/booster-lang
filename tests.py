import unittest
from parser import *
from interpreter import *


class InterpreterTest(unittest.TestCase):

    def test_set(self):
        i = Interpreter(parse_program("set x 3"))
        i.run()
        self.assertEqual(i.env, {"x": 3})

    def test_fibo_globals(self):
        i = Interpreter(
            [
                VarDef("lo", 0),
                VarDef("hi", 1),
                Label("fibo"),
                Print("lo"),
                VarDef("prev_hi", "hi"),
                Inc("hi", "lo"),
                VarDef("lo", "prev_hi"),
                If("hi", "<", 20, Goto("fibo")),
            ]
        )
        i.run()
        self.assertEqual(i.env["lo"], 13)
        self.assertEqual(i.env["hi"], 21)


if __name__ == "__main__":
    unittest.main()
