import unittest
from parser import *


class ParserTests(unittest.TestCase):

    def test_parse_skip(self):
        result = parse_program("")
        self.assertEqual(result, [Skip()])

    def test_parse_print(self):
        result = parse_program("print 42")
        self.assertEqual(result, [Print(42)])

    def test_parse_set(self):
        result = parse_program("set x 5")
        self.assertEqual(result, [VarDef("x", 5)])

    def test_parse_inc(self):
        result = parse_program("inc x 3")
        self.assertEqual(result, [Inc("x", 3)])

    def test_parse_dec(self):
        result = parse_program("dec x 2")
        self.assertEqual(result, [Dec("x", 2)])

    def test_parse_label(self):
        result = parse_program("label loop")
        self.assertEqual(result, [Label("loop")])

    def test_parse_goto(self):
        result = parse_program("goto loop")
        self.assertEqual(result, [Goto("loop")])

    def test_parse_if(self):
        result = parse_program("if 5 > 3 then print 1")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], If)

    def test_parse_halt(self):
        result = parse_program("halt")
        self.assertEqual(result, [Exit()])

    def test_parse_fun(self):
        result = parse_program("fun add a b")
        self.assertEqual(result, [Fun("add", ["a", "b"])])

    def test_parse_call(self):
        result = parse_program("call add 3 5")
        self.assertEqual(result, [Call("add", [3, 5])])

    def test_parse_return(self):
        result = parse_program("return")
        self.assertEqual(result, [Return()])

    def test_parse_multiple_statements(self):
        result = parse_program("set x 5; print x; halt")
        self.assertEqual(len(result), 3)

    def test_parse_error_invalid_statement(self):
        with self.assertRaises(ParseError):
            parse_program("invalid_command")


if __name__ == "__main__":
    unittest.main()
