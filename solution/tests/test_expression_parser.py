import unittest
from ..expression_parser import *


class ExpressionParserTest(unittest.TestCase):
    def test_identifier(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual("my_identifier3", parser.parse_identifier())

    def test_identifier_one_char(self):
        parser = ExpressionParser("a")
        self.assertEqual("a", parser.parse_identifier())

    def test_integer(self):
        parser = ExpressionParser("123")
        self.assertEqual(Int(123), parser.parse_int())

    def test_integer_fails(self):
        parser = ExpressionParser("abc")
        self.assertRaisesRegex(
            ParseException,
            "Expected some isdigit",
            lambda: parser.parse_int(),
        )

    def test_integer_followed_by_alpha_fails(self):
        parser = ExpressionParser("123a")
        self.assertRaisesRegex(
            ParseException,
            "Int cannot be followed by alphabetic character",
            lambda: parser.parse_int(),
        )

    def test_var(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual(Var("my_identifier3"), parser.parse_var())

    def test_str_lit(self):
        parser = ExpressionParser('"string $ literal %"')
        self.assertEqual(StrLit("string $ literal %"), parser.parse_str_lit())

    def test_str_lit_without_end(self):
        parser = ExpressionParser('"string $ literal %')
        self.assertRaisesRegex(
            ParseException,
            'Expected """: Unexpected end of input',
            lambda: parser.parse_str_lit(),
        )

    def test_bool_true(self):
        parser = ExpressionParser("true")
        self.assertEqual(Bool(True), parser.parse_bool())

    def test_bool_false(self):
        parser = ExpressionParser("false")
        self.assertEqual(Bool(False), parser.parse_bool())

    def test_add(self):
        parser = ExpressionParser("add a 2")
        self.assertEqual(BinOp("add", Var("a"), Int(2)), parser.parse_bin_op())

    def test_add_failure(self):
        parser = ExpressionParser("add a 2a")
        self.assertRaisesRegex(
            ParseException,
            'cannot be followed by alphabetic character at "2a"',
            lambda: parser.parse_bin_op(),
        )

    def test_math_expr(self):
        parser = ExpressionParser("add a sub b mul c div d e")
        self.assertEqual(
            BinOp(
                "add",
                Var("a"),
                BinOp(
                    "sub",
                    Var("b"),
                    BinOp(
                        "mul",
                        Var("c"),
                        BinOp("div", Var("d"), Var("e")),
                    ),
                ),
            ),
            parser.parse_expr(),
        )

    def test_math_sub_expr(self):
        parser = ExpressionParser("sub (add a b) c")
        self.assertEqual(
            BinOp(
                "sub",
                BinOp("add", Var("a"), Var("b")),
                Var("c"),
            ),
            parser.parse_expr(),
        )

    def test_list(self):
        parser = ExpressionParser('[1, "a", b, true]')
        self.assertEqual(
            List([Int(1), StrLit("a"), Var("b"), Bool(True)]),
            parser.parse_expr(),
        )

    def test_list_missing_end_str_lit_fail(self):
        parser = ExpressionParser('[1, "a, b, true]')
        self.assertRaisesRegex(
            ParseException,
            'Expected "]": Unexpected end of input',
            lambda: parser.parse_expr(),
        )

    def test_list_missing_comma_fail(self):
        parser = ExpressionParser('[1, "a" b, true]')
        self.assertRaisesRegex(
            ParseException,
            'Expected "]", got "b"',
            lambda: parser.parse_expr(),
        )

    def test_function_call(self):
        parser = ExpressionParser('call foo(1, a, true, "hello")')
        self.assertEqual(
            FunCall("foo", [Int(1), Var("a"), Bool(True), StrLit("hello")]),
            parser.parse_function_call(),
        )


if __name__ == "__main__":
    unittest.main()
