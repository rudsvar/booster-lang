from dataclasses import dataclass
import unittest
from expression import *
from parser import *


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

    def test_whitespace(self):
        parser = Parser(" \n ; ")
        self.assertEqual(" \n ", parser.whitespace())
        self.assertEqual(2, parser.line)
        self.assertEqual(2, parser.column)
        self.assertEqual("; ", parser.input)

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
        self.assertEqual(Int(123), parser.int())

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
        self.assertEqual(Var("my_identifier3"), parser.var())

    def test_str_lit(self):
        parser = ExpressionParser('"string $ literal %"')
        self.assertEqual(StrLit("string $ literal %"), parser.str_lit())

    def test_str_lit_without_end(self):
        parser = ExpressionParser('"string $ literal %')
        self.assertRaisesRegex(
            ParseException,
            'Expected """: Unexpected end of input',
            lambda: parser.str_lit(),
        )

    def test_add(self):
        parser = ExpressionParser("+ a 2")
        self.assertEqual(Add(Var("a"), Int(2)), parser.add())

    def test_add_failure(self):
        parser = ExpressionParser("+ a (2a)")
        self.assertRaisesRegex(
            ParseException,
            'cannot be followed by alphabetic character at "2a"',
            lambda: parser.add(),
        )

    def test_math_expr(self):
        parser = ExpressionParser("+ a - b * c / d e")
        self.assertEqual(
            Add(
                Var("a"),
                Sub(
                    Var("b"),
                    Mul(
                        Var("c"),
                        Div(Var("d"), Var("e")),
                    ),
                ),
            ),
            parser.expr(),
        )

    def test_math_sub_expr(self):
        parser = ExpressionParser("- (+ a b) c")
        self.assertEqual(
            Sub(
                Add(Var("a"), Var("b")),
                Var("c"),
            ),
            parser.expr(),
        )


class StatementParserTest(unittest.TestCase):
    def test_var_decl(self):
        parser = StatementParser("let x = 10;")
        self.assertEqual(VarDecl("x", Int(10)), parser.var_decl())

    def test_var_decl_fail(self):
        parser = StatementParser("let x =")
        self.assertRaisesRegex(
            ParseException, "Failed to parse expression", lambda: parser.var_decl()
        )

    def test_var_decl_deep_error_is_included(self):
        parser = StatementParser("let x = (+ 2 3a);")
        self.assertRaisesRegex(
            ParseException,
            r'at "\(\+ 2 3a".*at "\+ 2 3a".*at "3a"',
            lambda: parser.var_decl(),
        )

    def test_var_decl_keyword_cannot_be_followed_by_alnum(self):
        parser = StatementParser("letx = (+ 2 3);")
        self.assertRaisesRegex(
            ParseException,
            'Keyword "let" cannot be followed by "x"',
            lambda: parser.var_decl(),
        )

    def test_print(self):
        parser = StatementParser("print + 2 a;")
        self.assertEqual(Print(Add(Int(2), Var("a"))), parser.print())


if __name__ == "__main__":
    unittest.main()
