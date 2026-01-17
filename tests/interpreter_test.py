import unittest
from interpreter.interpret_exception import InterpretException
from parser.program import *
from interpreter.interpreter import Env
from interpreter import interpreter


class InterpreterTest(unittest.TestCase):

    def test_empty_program(self):
        program = ProgramParser("").parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(Env(), env)

    def test_variable_declaration(self):
        program = ProgramParser('let x = 10; let y = "Test";').parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual([{"x": 10, "y": "Test"}], env.scopes)

    def test_print(self):
        program = ProgramParser("shout add 2 3;").parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(Env(), env)

    def test_block(self):
        program = ProgramParser('let x = 10; { let y = "Test"; }').parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual([{"x": 10}], env.scopes)

    def test_undeclared_variable(self):
        program = ProgramParser("shout add 2 a;").parse_program()
        env = Env()
        self.assertRaisesRegex(
            InterpretException,
            'Undefined variable "a"',
            lambda: interpreter.exec_program(program, env),
        )

    def test_variables_are_removed_after_exiting_scope(self):
        program = ProgramParser(
            """
            let a = 3;
            {
                let b = 3;
                shout b;
            }
            shout a;
            shout b;
        """
        ).parse_program()
        env = Env()
        self.assertRaisesRegex(
            InterpretException,
            'Undefined variable "b"',
            lambda: interpreter.exec_program(program, env),
        )

    def test_addition(self):
        program = ProgramParser(
            "let x = 10; let y = 20; let z = add x y;"
        ).parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertTrue(30, env.lookup_var("z"))

    def test_list(self):
        program = ProgramParser('let x = [1, "a", true];').parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertTrue([1, "a", True], env.lookup_var("x"))

    def test_if_true_then(self):
        program = ProgramParser("let b = true; if b { shout b; }").parse_program()
        print(program)
        env = Env()
        interpreter.exec_program(program, env)

    def test_if_false_then(self):
        program = ProgramParser("let b = false; if b { shout b; }").parse_program()
        print(program)
        env = Env()
        interpreter.exec_program(program, env)

    def test_if_true_then_else(self):
        program = ProgramParser(
            "let b = true; if b { shout b; } else { shout undefined; }"
        ).parse_program()
        print(program)
        env = Env()
        interpreter.exec_program(program, env)

    def test_if_false_then_else(self):
        program = ProgramParser(
            "let b = false; if b { shout undefined; } else { shout b; }"
        ).parse_program()
        print(program)
        env = Env()
        interpreter.exec_program(program, env)

    def test_assignment(self):
        program = ProgramParser("let x = 3; { x = 4; }").parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(4, env.lookup_var("x"))

    def test_assignment_undefined_var(self):
        program = ProgramParser("let x = 3; { y = 4; }").parse_program()
        env = Env()
        self.assertRaisesRegex(
            InterpretException,
            'Undefined variable "y"',
            lambda: interpreter.exec_program(program, env),
        )

    def test_fun_decl(self):
        program = ProgramParser(
            "fun foo(x, y) { return add x y; } let x = call foo(1, 2);"
        ).parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(3, env.lookup_var("x"))

    def test_fun_decl_fibonacci(self):
        with open("examples/fibonacci.blang") as f:
            input = f.read()
        program = ProgramParser(input).parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(55, env.lookup_var("x"))

    def test_fun_decl_mutual_recursion(self):
        with open("examples/mutual_recursion.blang") as f:
            input = f.read()
        program = ProgramParser(input).parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(5, env.lookup_var("x"))

    def test_whilst(self):
        program = ProgramParser(
            "let x = 5; whilst neq x 0 { x = sub x 1; } shout x;"
        ).parse_program()
        env = Env()
        interpreter.exec_program(program, env)
        self.assertEqual(0, env.lookup_var("x"))


if __name__ == "__main__":
    unittest.main()
