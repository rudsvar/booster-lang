import unittest
from parser.basic import *


class BasicParserTest(unittest.TestCase):

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
        self.assertEqual("a", parser.while_satisfied(str.isalpha))
        self.assertEqual(1, parser.line)
        self.assertEqual(2, parser.column)

    def test_sat_resets_column_if_newline(self):
        parser = Parser("\nbc")
        self.assertEqual("\n", parser.while_satisfied(str.isascii))
        self.assertEqual(2, parser.line)
        self.assertEqual(1, parser.column)

    def test_sat_fails_if_check_fails(self):
        parser = Parser("abc")
        self.assertRaisesRegex(
            ParseException,
            r"isnumeric\('a'\) failed",
            lambda: parser.while_satisfied(str.isnumeric),
        )

    def test_sat_fails_if_no_input(self):
        parser = Parser("")
        self.assertRaises(ParseException, lambda: parser.while_satisfied(str.isalpha))

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
        self.assertEqual("123", parser.parse_digits())

    def test_digits_fails(self):
        parser = Parser("abc123")
        self.assertRaisesRegex(
            ParseException, "Expected some isdigit", parser.parse_digits
        )

    def test_alphas(self):
        parser = Parser("abc123")
        self.assertEqual("abc", parser.parse_alphas())

    def test_alphas_fails(self):
        parser = Parser("123abc")
        self.assertRaisesRegex(
            ParseException, "Expected some isalpha", parser.parse_alphas
        )

    def test_whitespace(self):
        parser = Parser(" \n ; ")
        self.assertEqual(" \n ", parser.parse_whitespace())
        self.assertEqual(2, parser.line)
        self.assertEqual(2, parser.column)
        self.assertEqual("; ", parser.input)

    def test_exactly(self):
        parser = Parser("Hello123")
        self.assertEqual("Hello1", parser.parse_string("Hello1"))
        self.assertEqual(1, parser.line)
        self.assertEqual(7, parser.column)
        self.assertEqual("23", parser.input)
        self.assertTrue(parser.has_consumed)

    def test_exactly_fails(self):
        parser = Parser("Hel8lo123")
        self.assertRaisesRegex(
            ParseException,
            'Expected "Hello1", got "Hel8lo"',
            lambda: parser.parse_string("Hello1"),
        )

    def test_symbol(self):
        parser = Parser("(  a )")
        self.assertEqual("(", parser.parse_symbol("("))
        self.assertEqual("a )", parser.input)

    def test_separated_by(self):
        parser = Parser("a, b, c")
        self.assertEqual(
            ["a", "b", "c"], parser.separated_by(parser.parse_identifier, ",")
        )

    def test_separated_by_trailing(self):
        parser = Parser("a, b, c,")
        self.assertEqual(
            ["a", "b", "c"], parser.separated_by(parser.parse_identifier, ",")
        )

    def test_keyword(self):
        parser = Parser("let ")
        self.assertEqual("let", parser.parse_keyword("let"))
        self.assertEqual("", parser.input)

    def test_keyword_alternatives(self):
        parser = Parser("lettuce ")
        self.assertEqual(
            "lettuce",
            parser.one_of(
                [
                    lambda: parser.parse_keyword("let"),
                    lambda: parser.parse_keyword("lettuce"),
                    lambda: parser.parse_keyword("tomato"),
                ]
            ),
        )
        self.assertEqual("", parser.input)


if __name__ == "__main__":
    unittest.main()
