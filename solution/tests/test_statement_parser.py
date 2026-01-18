import unittest
from statement_parser import *


class StatementParserTest(unittest.TestCase):
    def test_var_decl(self):
        parser = StatementParser("let x = 10;")
        self.assertEqual(VariableDefinition("x", 10), parser.parse_var_def())

    def test_var_decl_bool(self):
        parser = StatementParser("let x = true;")
        self.assertEqual(VariableDefinition("x", True), parser.parse_var_def())

    def test_var_decl_fail(self):
        parser = StatementParser("let x =")
        self.assertRaisesRegex(
            ParseException, "Failed to parse expression", lambda: parser.parse_var_def()
        )

    def test_var_decl_deep_error_is_included(self):
        parser = StatementParser("let x = (add 2 3!);")
        self.assertRaisesRegex(
            ParseException,
            r'Expected "\)", got "!"',
            lambda: parser.parse_var_def(),
        )

    def test_var_decl_keyword_cannot_be_followed_by_alnum(self):
        parser = StatementParser("letx = (add 2 3);")
        self.assertRaisesRegex(
            ParseException,
            'Keyword "let" cannot be followed by "x"',
            lambda: parser.parse_var_def(),
        )

    def test_shout(self):
        parser = StatementParser("shout add 2 a;")
        self.assertEqual(
            Shout(BinaryOperation("add", 2, Variable("a"))), parser.parse_shout()
        )

    def test_if_then(self):
        parser = StatementParser('if b { shout "Yes!"; }')
        self.assertEqual(
            If(Variable("b"), Block([Shout("Yes!")]), None),
            parser.parse_if(),
        )

    def test_if_then_else(self):
        parser = StatementParser('if b { shout "Yes!"; } else { shout "Nah"; }')
        self.assertEqual(
            If(Variable("b"), Block([Shout("Yes!")]), Block([Shout("Nah")])),
            parser.parse_if(),
        )

    def test_whilst(self):
        parser = StatementParser("whilst b { x = sub x 1; }")
        self.assertEqual(
            Whilst(
                Variable("b"),
                Block([Assignment("x", BinaryOperation("sub", Variable("x"), 1))]),
            ),
            parser.parse_whilst(),
        )


if __name__ == "__main__":
    unittest.main()
