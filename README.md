# Booster Lang

There are three main parts to the solution directory.

- Parsers for transforming source code into an Abstract Syntax Tree (AST), like the classes `Expr` and `Stmt`.
- An interpreter for evaluating expressions and executing statements.
- An entrypoint (`main.py`) to read files, parse them, and run them with the interpreter.

## Command Line Usage

Each parser and the interpreter can be run directly from the command line:
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
