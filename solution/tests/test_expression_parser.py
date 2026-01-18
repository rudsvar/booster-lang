import unittest
from expression_parser import *


class ExpressionParserTest(unittest.TestCase):
    def test_identifier(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual("my_identifier3", parser.parse_identifier())

    def test_identifier_one_char(self):
        parser = ExpressionParser("a")
        self.assertEqual("a", parser.parse_identifier())

    def test_integer(self):
        parser = ExpressionParser("123")
        self.assertEqual(123, parser.parse_int())

    def test_integer_fails(self):
        parser = ExpressionParser("abc")
        self.assertRaisesRegex(
            ParseException,
            "Expected some isdigit",
            lambda: parser.parse_int(),
        )

    def test_var(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual(Variable("my_identifier3"), parser.parse_var())

    def test_string_literal(self):
        parser = ExpressionParser('"string $ literal %"')
        self.assertEqual("string $ literal %", parser.parse_string_literal())

    def test_string_literal_without_end(self):
        parser = ExpressionParser('"string $ literal %')
        self.assertRaisesRegex(
            ParseException,
            'Expected """: Unexpected end of input',
            lambda: parser.parse_string_literal(),
        )

    def test_bool_true(self):
        parser = ExpressionParser("true")
        self.assertEqual(True, parser.parse_bool())

    def test_bool_false(self):
        parser = ExpressionParser("false")
        self.assertEqual(False, parser.parse_bool())

    def test_add(self):
        parser = ExpressionParser("add a 2")
        self.assertEqual(
            BinaryOperation("add", Variable("a"), 2), parser.parse_binary_operation()
        )

    def test_add_failure(self):
        parser = ExpressionParser("add a !")
        self.assertRaisesRegex(
            ParseException,
            "Failed to parse expression",
            lambda: parser.parse_binary_operation(),
        )

    def test_math_expr(self):
        parser = ExpressionParser("add a sub b mul c div d e")
        self.assertEqual(
            BinaryOperation(
                "add",
                Variable("a"),
                BinaryOperation(
                    "sub",
                    Variable("b"),
                    BinaryOperation(
                        "mul",
                        Variable("c"),
                        BinaryOperation("div", Variable("d"), Variable("e")),
                    ),
                ),
            ),
            parser.parse_expr(),
        )

    def test_math_sub_expr(self):
        parser = ExpressionParser("sub (add a b) c")
        self.assertEqual(
            BinaryOperation(
                "sub",
                BinaryOperation("add", Variable("a"), Variable("b")),
                Variable("c"),
            ),
            parser.parse_expr(),
        )

    def test_list(self):
        parser = ExpressionParser('[1, "a", b, true]')
        self.assertEqual(
            [1, "a", Variable("b"), True],
            parser.parse_expr(),
        )

    def test_list_missing_end_string_literal_fail(self):
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
            FunctionCall("foo", [1, Variable("a"), True, "hello"]),
            parser.parse_function_call(),
        )


if __name__ == "__main__":
    unittest.main()
