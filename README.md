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
In any of the following tasks, you can rename keywords, switch out symbols, or change the behavior, as long as it don't cause ambiguity for the parser.
For example, instead of `print`, the example solution has the `shout` keyword that prints a stringified uppercase version of the input.

1. Implement `parse_int`, `eval_int`, `parse_shout` and `exec_shout`. Then try to run the interpreter with the input `shout 42;`
    - Optional: Implement `parse_bool` to be able to run `shout true;`
    - Optional: Implement `parse_string_literal` to be able to run `shout "Hello World!"`
2. Implement `parse_var`, `parse_var_def` and `exec_var_def` to be able to run `let x = 10; shout x;`
3. Implement `parse_binary_operation` and `eval_binary_operation`. Then try to run the interpreter with the input `shout add 2 3;`
    - Optional: Add more operators such as `eq` (equal), `!=` (not equal), `<` (less than).
4. Implement `parse_if` and `exec_if`. Then try to run the interpreter with the input `if eq 2 3 { shout "True!"; }`
    - Optional: Try to parse an optional `else`-block after the if.
5. Implement `parse_whilst` and `exec_whilst`. Then try to run the interpreter with the input `let x = 0; whilst neq x 10 { shout x; x = add x 1; }`
6. Implement `parse_function_definition`, `parse_function_call`, `eval_function_call`, and `exec_function_definition`. Then try to run the interpreter with the input `fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;`