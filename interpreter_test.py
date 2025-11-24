import unittest
from expression import *
from parser import *
from interpreter import *


class InterpreterTest(unittest.TestCase):

    def test_empty_program(self):
        program = ProgramParser("").program()
        env = [{}]
        exec(program, env)
        self.assertEqual([{}], env)

    def test_variable_declaration(self):
        program = ProgramParser('let x = 10; let y = "Test";').program()
        env = [{}]
        exec(program, env)
        self.assertEqual([{"x": 10, "y": "Test"}], env)

    def test_print(self):
        program = ProgramParser("print + 2 3;").program()
        env = [{}]
        exec(program, env)
        self.assertEqual([{}], env)

    def test_block(self):
        program = ProgramParser('let x = 10; { let y = "Test"; }').program()
        env = [{}]
        exec(program, env)
        self.assertEqual([{"x": 10}], env)

    def test_undeclared_variable(self):
        program = ProgramParser("print + 2 a;").program()
        self.assertRaisesRegex(
            InterpretException, 'Undefined variable "a"', lambda: exec(program, [{}])
        )

    def test_variables_are_removed_after_exiting_scope(self):
        program = ProgramParser(
            """
            let a = 3;
            {
                let b = 3;
                print(b);
            }
            print(a);
            print(b);
        """
        ).program()
        self.assertRaisesRegex(
            InterpretException, 'Undefined variable "b"', lambda: exec(program, [{}])
        )

    def test_addition(self):
        program = ProgramParser("let x = 10; let y = 20; let z = + x y;").program()
        env = [{}]
        exec(program, env)
        self.assertTrue(30, lookup(env, "z"))

    def test_concatenation(self):
        program = ProgramParser(
            'let x = "Hello "; let y = " world!"; let z = + x y;'
        ).program()
        env = [{}]
        exec(program, env)
        self.assertTrue("Hello world!", lookup(env, "z"))

    def test_list(self):
        program = ProgramParser('let x = [1, "a", true];').program()
        env = [{}]
        exec(program, env)
        self.assertTrue([1, "a", True], lookup(env, "x"))

    def test_if_true_then(self):
        program = ProgramParser("let b = true; if b { print b; }").program()
        print(program)
        env = [{}]
        exec(program, env)

    def test_if_false_then(self):
        program = ProgramParser("let b = false; if b { print b; }").program()
        print(program)
        env = [{}]
        exec(program, env)

    def test_if_true_then_else(self):
        program = ProgramParser(
            "let b = true; if b { print b; } else { print undefined; }"
        ).program()
        print(program)
        env = [{}]
        exec(program, env)

    def test_if_false_then_else(self):
        program = ProgramParser(
            "let b = false; if b { print undefined; } else { print b; }"
        ).program()
        print(program)
        env = [{}]
        exec(program, env)

    def test_assignment(self):
        program = ProgramParser("let x = 3; { x = 4; }").program()
        env = [{}]
        exec(program, env)
        self.assertEqual(4, lookup(env, "x"))

    def test_assignment_undefined_var(self):
        program = ProgramParser("let x = 3; { y = 4; }").program()
        self.assertRaisesRegex(
            InterpretException, 'Undefined variable "y"', lambda: exec(program, [{}])
        )

    def test_fun_decl(self):
        program = ProgramParser(
            "fun foo(x, y) { return + x y; } let x = foo(1, 2);"
        ).program()
        env = [{}]
        exec(program, env)
        self.assertEqual(3, lookup(env, "x"))

    def test_fun_decl_fibonacci(self):
        input = open("examples/fibonacci.blang").read()
        program = ProgramParser(input).program()
        env = [{}]
        exec(program, env)
        self.assertEqual(55, lookup(env, "x"))

    def test_fun_decl_mutual_recursion(self):
        input = open("examples/mutual_recursion.blang").read()
        program = ProgramParser(input).program()
        env = [{}]
        exec(program, env)
        self.assertEqual(5, lookup(env, "x"))


if __name__ == "__main__":
    unittest.main()
