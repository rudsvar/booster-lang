import unittest
from interpreter import *


class TestInterpreter(unittest.TestCase):

    def test_set(self):
        i = Interpreter([Set("x", 3)])
        i.run()
        self.assertEqual(i.env, {"x", 3})

    def test_fibo_globals(self):
        i = Interpreter(
            [
                Set("lo", 0),
                Set("hi", 1),
                Label("fibo"),
                Print("lo"),
                Set("prev_hi", "hi"),
                Add("hi", "lo"),
                Set("lo", "prev_hi"),
                Jlt("hi", 20, "fibo"),
            ]
        )
        i.run()
        self.assertEqual(i.env["lo"], 13)
        self.assertEqual(i.env["hi"], 21)


if __name__ == "__main__":
    unittest.main()
