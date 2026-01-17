# Booster Lang

There are three main parts to the solution directory.

- Parsers for transforming source code into an Abstract Syntax Tree (AST), like the classes `Expr` and `Stmt`.
- An interpreter for evaluating expressions and executing statements.
- An entrypoint (`main.py`) to read files, parse them, and run them with the interpreter.