import unittest
from parser import *
from interpreter import *
from io import StringIO
import sys
import parser as parser_module


class InterpreterTests(unittest.TestCase):

    def setUp(self):
        parser_module.debug = True

    def tearDown(self):
        parser_module.debug = False

    def test_skip(self):
        i = Interpreter([Skip()])
        i.execute_program()
        self.assertEqual(i.env, {})

    def test_print(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        i = Interpreter([Let("x", 42), Print("x")])
        i.execute_program()
        sys.stdout = sys.__stdout__
        self.assertIn("42", captured_output.getvalue())

    def test_inc(self):
        i = Interpreter([Let("x", 5), Inc("x", 3)])
        i.execute_program()
        self.assertEqual(i.env["x"], 8)

    def test_dec(self):
        i = Interpreter([Let("x", 10), Dec("x", 3)])
        i.execute_program()
        self.assertEqual(i.env["x"], 7)

    def test_mul(self):
        i = Interpreter([Let("x", 6), Mul("x", 7)])
        i.execute_program()
        self.assertEqual(i.env["x"], 42)

    def test_swap(self):
        i = Interpreter([Let("x", 10), Let("y", 20), Swap("x", "y")])
        i.execute_program()
        self.assertEqual(i.env["x"], 20)
        self.assertEqual(i.env["y"], 10)

    def test_label(self):
        i = Interpreter([Label("start"), Let("x", 1)])
        i.execute_program()
        self.assertEqual(i.env["x"], 1)

    def test_goto(self):
        i = Interpreter([Goto("end"), Let("x", 1), Label("end"), Let("x", 2)])
        i.execute_program()
        self.assertEqual(i.env["x"], 2)

    def test_if_true(self):
        i = Interpreter([If(5, ">", 3, Let("x", 1))])
        i.execute_program()
        self.assertEqual(i.env["x"], 1)

    def test_if_false(self):
        i = Interpreter([If(2, ">", 3, Let("x", 1))])
        i.execute_program()
        self.assertEqual(i.env, {})

    def test_exit(self):
        i = Interpreter([Let("x", 1), Exit(), Let("x", 2)])
        i.execute_program()
        self.assertEqual(i.env["x"], 1)

    def test_proc_and_call(self):
        i = Interpreter(
            [
                Goto("main"),
                Proc("add", ["a", "b"]),
                Let("result", "a"),
                Inc("result", "b"),
                Return(),
                Label("main"),
                Call("add", [3, 5]),
            ]
        )
        i.execute_program()
        # After call, position should be at return address
        self.assertIn("result", i.env)


if __name__ == "__main__":
    unittest.main()
