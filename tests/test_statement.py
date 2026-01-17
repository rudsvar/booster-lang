import unittest
from parser.statement import *


class StatementParserTest(unittest.TestCase):
    def test_var_decl(self):
        parser = StatementParser("let x = 10;")
        self.assertEqual(VarDef("x", Int(10)), parser.parse_var_def())

    def test_var_decl_bool(self):
        parser = StatementParser("let x = true;")
        self.assertEqual(VarDef("x", Bool(True)), parser.parse_var_def())

    def test_var_decl_fail(self):
        parser = StatementParser("let x =")
        self.assertRaisesRegex(
            ParseException, "Failed to parse expression", lambda: parser.parse_var_def()
        )

    def test_var_decl_deep_error_is_included(self):
        parser = StatementParser("let x = (+ 2 3a);")
        self.assertRaisesRegex(
            ParseException,
            r'at "\(\+ 2 3a".*at "\+ 2 3a".*at "3a"',
            lambda: parser.parse_var_def(),
        )

    def test_var_decl_keyword_cannot_be_followed_by_alnum(self):
        parser = StatementParser("letx = (+ 2 3);")
        self.assertRaisesRegex(
            ParseException,
            'Keyword "let" cannot be followed by "x"',
            lambda: parser.parse_var_def(),
        )

    def test_shout(self):
        parser = StatementParser("shout + 2 a;")
        self.assertEqual(Shout(BinOp("+", Int(2), Var("a"))), parser.parse_shout())

    def test_if_then(self):
        parser = StatementParser('if b { shout "Yes!"; }')
        self.assertEqual(
            If(Var("b"), Block([Shout(StrLit("Yes!"))]), None),
            parser.parse_if(),
        )

    def test_if_then_else(self):
        parser = StatementParser('if b { shout "Yes!"; } else { shout "Nah"; }')
        self.assertEqual(
            If(Var("b"), Block([Shout(StrLit("Yes!"))]), Block([Shout(StrLit("Nah"))])),
            parser.parse_if(),
        )


if __name__ == "__main__":
    unittest.main()
