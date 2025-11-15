from dataclasses import dataclass
import unittest
import expression
from parser2 import Parser, ParseException, ExpressionParser


class ParserTest(unittest.TestCase):

    def test_peek_gets_char(self):
        parser = Parser("abc")
        self.assertEqual("a", parser.peek())
        self.assertEqual(1, parser.line)
        self.assertEqual(1, parser.column)

    def test_peek_fails_if_no_input(self):
        parser = Parser("")
        self.assertRaises(ParseException, parser.peek)

    def test_sat_gets_matching_char(self):
        parser = Parser("abc")
        self.assertEqual("a", parser.sat(str.isalpha))
        self.assertEqual(1, parser.line)
        self.assertEqual(2, parser.column)

    def test_sat_resets_column_if_newline(self):
        parser = Parser("\nbc")
        self.assertEqual("\n", parser.sat(str.isascii))
        self.assertEqual(2, parser.line)
        self.assertEqual(1, parser.column)

    def test_sat_fails_if_check_fails(self):
        parser = Parser("abc")
        self.assertRaisesRegex(
            ParseException,
            r"isnumeric\('a'\) failed",
            lambda: parser.sat(str.isnumeric),
        )

    def test_sat_fails_if_no_input(self):
        parser = Parser("")
        self.assertRaises(ParseException, lambda: parser.sat(str.isalpha))

    def test_many_digits(self):
        parser = Parser("123abc")
        self.assertEqual("123", parser.zero_or_more(str.isdigit))

    def test_many_empty(self):
        parser = Parser("abc")
        self.assertEqual("", parser.zero_or_more(str.isdigit))

    def test_some_alphas(self):
        parser = Parser("abc123")
        self.assertEqual("abc", parser.zero_or_more(str.isalpha))

    def test_digits(self):
        parser = Parser("123abc")
        self.assertEqual("123", parser.digits())

    def test_digits_fails(self):
        parser = Parser("abc123")
        self.assertRaisesRegex(ParseException, "Expected some isdigit", parser.digits)

    def test_alphas(self):
        parser = Parser("abc123")
        self.assertEqual("abc", parser.alphas())

    def test_alphas_fails(self):
        parser = Parser("123abc")
        self.assertRaisesRegex(ParseException, "Expected some isalpha", parser.alphas)

    def test_identifier(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual("my_identifier3", parser.identifier())

    def test_identifier_one_char(self):
        parser = ExpressionParser("a")
        self.assertEqual("a", parser.identifier())

    def test_exactly(self):
        parser = Parser("Hello123")
        self.assertEqual("Hello1", parser.exactly("Hello1"))
        self.assertEqual(1, parser.line)
        self.assertEqual(7, parser.column)
        self.assertEqual("23", parser.input)
        self.assertTrue(parser.has_consumed)

    def test_exactly_fails(self):
        parser = Parser("Hel8lo123")
        self.assertRaisesRegex(
            ParseException,
            'Expected "Hello1", got "Hel8lo"',
            lambda: parser.exactly("Hello1"),
        )

    def test_symbol(self):
        parser = Parser("(  a )")
        self.assertEqual("(", parser.symbol("("))
        self.assertEqual("a )", parser.input)


class ExpressionParserTest(unittest.TestCase):
    def test_integer(self):
        parser = ExpressionParser("123")
        self.assertEqual(expression.Int(123), parser.int())

    def test_integer_fails(self):
        parser = ExpressionParser("abc")
        self.assertRaisesRegex(
            ParseException,
            "Expected some isdigit",
            lambda: parser.int(),
        )

    def test_integer_followed_by_alpha_fails(self):
        parser = ExpressionParser("123a")
        self.assertRaisesRegex(
            ParseException,
            "Int cannot be followed by alphabetic character",
            lambda: parser.int(),
        )

    def test_var(self):
        parser = ExpressionParser("my_identifier3")
        self.assertEqual(expression.Var("my_identifier3"), parser.var())

    def test_str_lit(self):
        parser = ExpressionParser('"string $ literal %"')
        self.assertEqual(expression.StrLit("string $ literal %"), parser.str_lit())

    def test_str_lit_without_end(self):
        parser = ExpressionParser('"string $ literal %')
        self.assertRaisesRegex(
            ParseException, 'Expected """, got ""', lambda: parser.str_lit()
        )

    def test_add(self):
        parser = ExpressionParser("+ a 2")
        self.assertEqual(
            expression.Add(expression.Var("a"), expression.Int(2)), parser.add()
        )

    def test_math_expr(self):
        parser = ExpressionParser("+ a - b * c / d e")
        self.assertEqual(
            expression.Add(
                expression.Var("a"),
                expression.Sub(
                    expression.Var("b"),
                    expression.Mul(
                        expression.Var("c"),
                        expression.Div(expression.Var("d"), expression.Var("e")),
                    ),
                ),
            ),
            parser.expr(),
        )

    def test_math_sub_expr(self):
        parser = ExpressionParser("- (+ a b) c")
        self.assertEqual(
            expression.Sub(
                expression.Add(expression.Var("a"), expression.Var("b")),
                expression.Var("c"),
            ),
            parser.expr(),
        )


if __name__ == "__main__":
    unittest.main()
