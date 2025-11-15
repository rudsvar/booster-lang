from dataclasses import dataclass
import unittest
from parser2 import Parser, ParseException


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
        self.assertEqual("123", parser.many(str.isdigit))

    def test_many_empty(self):
        parser = Parser("abc")
        self.assertEqual("", parser.many(str.isdigit))

    def test_some_alphas(self):
        parser = Parser("abc123")
        self.assertEqual("abc", parser.many(str.isalpha))

    def test_digits(self):
        parser = Parser("123abc")
        self.assertEqual("123", parser.digits())

    def test_digits_fails(self):
        parser = Parser("abc123")
        self.assertRaisesRegex(ParseException, "Expected some digits", parser.digits)

    def test_alphas(self):
        parser = Parser("abc123")
        self.assertEqual("abc", parser.alphas())

    def test_alphas_fails(self):
        parser = Parser("123abc")
        self.assertRaisesRegex(ParseException, "Expected some alphas", parser.alphas)

    def test_exactly(self):
        parser = Parser("Hello123")
        self.assertEqual("Hello1", parser.exactly("Hello1"))
        self.assertEqual(1, parser.line)
        self.assertEqual(7, parser.column)

    def test_exactly_fails(self):
        parser = Parser("Hel8lo123")
        self.assertRaisesRegex(
            ParseException,
            'Expected "Hello1", got "Hel8lo..."',
            lambda: parser.exactly("Hello1"),
        )


if __name__ == "__main__":
    unittest.main()
