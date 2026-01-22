import unittest
from base_parser import *


class BaseParserTest(unittest.TestCase):

    def test_peek_gets_char(self):
        parser = BaseParser("abc")
        self.assertEqual("a", parser.peek())
        self.assertEqual(1, parser.line)
        self.assertEqual(1, parser.column)

    def test_peek_fails_if_no_input(self):
        parser = BaseParser("")
        self.assertRaises(ParseException, parser.peek)

    def test_parse_until(self):
        parser = BaseParser("abc! ")
        abc = parser.parse_until("!")
        self.assertEqual("abc", abc)

    def test_digits(self):
        parser = BaseParser("123abc")
        self.assertEqual("123", parser.parse_digits())

    def test_digits_fails(self):
        parser = BaseParser("abc123")
        self.assertRaisesRegex(
            ParseException, "Expected some isdigit", parser.parse_digits
        )

    def test_alphas(self):
        parser = BaseParser("abc123")
        self.assertEqual("abc", parser.parse_alphabetics())

    def test_alphas_fails(self):
        parser = BaseParser("123abc")
        self.assertRaisesRegex(
            ParseException, "Expected some isalpha", parser.parse_alphabetics
        )

    def test_whitespace(self):
        parser = BaseParser(" \n ; ")
        parser.parse_whitespace()
        self.assertEqual(2, parser.line)
        self.assertEqual(2, parser.column)
        self.assertEqual("; ", parser.input)

    def test_exactly(self):
        parser = BaseParser("Hello123")
        self.assertEqual("Hello1", parser.parse_string("Hello1"))
        self.assertEqual(1, parser.line)
        self.assertEqual(7, parser.column)
        self.assertEqual("23", parser.input)
        self.assertTrue(parser.has_consumed)

    def test_exactly_fails(self):
        parser = BaseParser("Hel8lo123")
        self.assertRaisesRegex(
            ParseException,
            'Expected "Hello1", got "Hel8lo"',
            lambda: parser.parse_string("Hello1"),
        )

    def test_symbol(self):
        parser = BaseParser("(  a )")
        self.assertEqual("(", parser.parse_symbol("("))
        self.assertEqual("a )", parser.input)

    def test_separated_by(self):
        parser = BaseParser("a, b, c")
        self.assertEqual(
            ["a", "b", "c"], parser.separated_by(parser.parse_identifier, ",")
        )

    def test_separated_by_trailing(self):
        parser = BaseParser("a, b, c,")
        self.assertEqual(
            ["a", "b", "c"], parser.separated_by(parser.parse_identifier, ",")
        )

    def test_keyword(self):
        parser = BaseParser("let ")
        self.assertEqual("let", parser.parse_keyword("let"))
        self.assertEqual("", parser.input)

    def test_keyword_alternatives(self):
        parser = BaseParser("lettuce ")
        self.assertEqual(
            "lettuce",
            parser.any(
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
