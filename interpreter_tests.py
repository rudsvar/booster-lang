import unittest
from parser import *
from interpreter import *
from io import StringIO
import sys
import parser as parser_module


class InterpreterTests(unittest.TestCase):

    def setUp(self):
        parser_module.DEBUG = True

    def tearDown(self):
        parser_module.DEBUG = False

    def test_skip(self):
        i = Interpreter([Skip()])
        i.run()
        self.assertEqual(i.env, {})

    def test_print(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        i = Interpreter([VarDef("x", 42), Print("x")])
        i.run()
        sys.stdout = sys.__stdout__
        self.assertIn("42", captured_output.getvalue())

    def test_inc(self):
        i = Interpreter([VarDef("x", 5), Inc("x", 3)])
        i.run()
        self.assertEqual(i.env["x"], 8)

    def test_dec(self):
        i = Interpreter([VarDef("x", 10), Dec("x", 3)])
        i.run()
        self.assertEqual(i.env["x"], 7)

    def test_label(self):
        i = Interpreter([Label("start"), VarDef("x", 1)])
        i.run()
        self.assertEqual(i.env["x"], 1)

    def test_goto(self):
        i = Interpreter([Goto("end"), VarDef("x", 1), Label("end"), VarDef("x", 2)])
        i.run()
        self.assertEqual(i.env["x"], 2)

    def test_if_true(self):
        i = Interpreter([If(5, ">", 3, VarDef("x", 1))])
        i.run()
        self.assertEqual(i.env["x"], 1)

    def test_if_false(self):
        i = Interpreter([If(2, ">", 3, VarDef("x", 1))])
        i.run()
        self.assertEqual(i.env, {})

    def test_exit(self):
        i = Interpreter([VarDef("x", 1), Exit(), VarDef("x", 2)])
        i.run()
        self.assertEqual(i.env["x"], 1)

    def test_fun_and_call(self):
        i = Interpreter(
            [
                Goto("main"),
                Fun("add", ["a", "b"]),
                VarDef("result", "a"),
                Inc("result", "b"),
                Return(),
                Label("main"),
                Call("add", [3, 5]),
            ]
        )
        i.run()
        # After call, position should be at return address
        self.assertIn("result", i.env)


if __name__ == "__main__":
    unittest.main()
