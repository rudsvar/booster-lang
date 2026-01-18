# Booster Lang

There are two main parts to the solution directory.

- Parsers for transforming source code into types we can work with.
- An interpreter for evaluating expressions and executing statements.

The parsers and the interpreter can be run directly from the command line.
Note that you might have to use `python` instead of `python3`.

### Expression Parser
Parse a single expression:
```bash
python3 solution/expression_parser.py "42"
python3 solution/expression_parser.py "add 2 3"
python3 solution/expression_parser.py "[1, 2, 3]"
```

### Statement Parser
Parse a single statement:
```bash
python3 solution/statement_parser.py "let x = 5;"
python3 solution/statement_parser.py "shout x;"
python3 solution/statement_parser.py "if true { let y = 10; }"
```

### Program Parser
Parse a complete program:
```bash
python3 solution/program_parser.py examples/fibonacci.blang
python3 solution/program_parser.py "let x = 5; shout x;"
```

### Interpreter
Parse and execute a program:
```bash
python3 solution/interpreter.py examples/fibonacci.blang
python3 solution/interpreter.py "let x = 5; shout x;"
```

## Tasks

The tasks will mostly switch between the three main parts to continuously extend the language as you implement it.
You don't need to do them in this order. You can try to run what you would like to have work, then implement what fails.

1. Implement `parse_int`, `eval_int`, `parse_shout` and `exec_shout`. Then try to run the interpreter with the input `shout 42;`
    - Optional: Implement `parse_bool` to be able to run `shout true;`
    - Optional: Implement `parse_string_literal` to be able to run `shout "Hello World!"`
2. Implement `parse_var`, `parse_var_def` and `exec_var_def` to be able to run `let x = 10; shout x;`