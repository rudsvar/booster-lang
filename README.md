# Booster Lang

There are two main parts to the solution directory.

- Parsers for transforming source code into types we can work with.
- An interpreter for evaluating expressions and executing statements.

The parsers and the interpreter can be run directly from the command line.
Note that you might have to use `python` instead of `python3`.

### Expression Evaluator
Evaluate a single expression:
```bash
python3 solution/expression_evaluator.py "42"
python3 solution/expression_evaluator.py "add 2 3"
python3 solution/expression_evaluator.py "[1, 2, 3]"
```

### Statement Executor
Execute a single statement:
```bash
python3 solution/statement_executor.py "let x = 5;"
python3 solution/statement_executor.py "shout x;"
python3 solution/statement_executor.py "if true { let y = 10; }"
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

1. **Print integers and basic types**
   
   Run: `python3 solution/interpreter.py exec "shout 42;"`
   
   - Implement `parse_int` and test with:
     ```bash
     python3 solution/expression_parser.py "42"
     ```
   - Implement `eval_int` and test with:
     ```bash
     python3 solution/expression_evaluator.py "42"
     ```
   - Implement `parse_shout` and test with:
     ```bash
     python3 solution/statement_parser.py "shout 42"
     ```
   - Implement `exec_shout` and run:
     ```bash
     python3 solution/interpreter.py "shout 42;"
     ```
   - Optional: Implement `parse_bool` and `eval_bool` to run `shout true;`
   - Optional: Implement `parse_string_literal` and `eval_string` to run `shout "Hello World!"`

2. **Variable definitions and lookups**
   
   Run: `python3 solution/interpreter.py exec "let x = 10; shout x;"`
   
   - Implement `parse_var` and test with:
     ```bash
     python3 solution/expression_evaluator.py "x"
     ```
   - Implement `parse_var_def` and test with:
     ```bash
     python3 solution/statement_executor.py "let x = 10;"
     ```
   - Implement `define_var`, `lookup_var`, `eval_var`, and `exec_var_def` and run:
     ```bash
     python3 solution/interpreter.py "let x = 10; shout x;"
     ```

3. **Binary operations**
   
   Run: `python3 solution/interpreter.py exec "shout add 2 3;"`
   
   - Implement `parse_binary_operation` and test with:
     ```bash
     python3 solution/expression_evaluator.py "add 2 3"
     ```
   - Implement `eval_binary_operation` and run:
     ```bash
     python3 solution/expression_evaluator.py "add 2 3"
     ```
     Or execute with:
     ```bash
     python3 solution/interpreter.py "shout add 2 3;"
     ```
   - Optional: Add more operators such as `eq` (equal), `neq` (not equal), `<` (less than).

4. **Conditionals**
   
   Run: `python3 solution/interpreter.py exec "if eq 2 3 { shout \"True!\"; }"`
   
   - Implement `parse_if` and test with:
     ```bash
     python3 solution/statement_executor.py "if eq 2 3 { shout \"True!\"; }"
     ```
   - Implement `exec_if` and run:
     ```bash
     python3 solution/interpreter.py "if eq 2 3 { shout \"True!\"; }"
     ```
   - Optional: Implement parsing an optional `else`-block after the if.

5. **Loops and variable assignment**
   
   Run: `python3 solution/interpreter.py exec "let x = 0; whilst neq x 10 { shout x; x = add x 1; }"`
   
   - Implement `parse_assignment` and `parse_whilst` and test with:
     ```bash
     python3 solution/statement_executor.py "x = add x 1;"
     python3 solution/statement_executor.py "whilst neq x 10 { shout x; }"
     ```
   - Implement `exec_assignment`, `exec_whilst`, and `assign_var` and run:
     ```bash
     python3 solution/interpreter.py "let x = 0; whilst neq x 10 { shout x; x = add x 1; }"
     ```

6. **Functions**
   
   Run: `python3 solution/interpreter.py exec "fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;"`
   
   - Implement `parse_function_call` and test with:
     ```bash
     python3 solution/expression_evaluator.py "call add(2, 3)"
     ```
   - Implement `parse_function_definition` and test with:
     ```bash
     python3 solution/statement_executor.py "fun add(x, y) { return x y; }"
     ```
   - Implement `eval_function_call`, `exec_function_definition` and run:
     ```bash
     python3 solution/expression_evaluator.py "call add(2, 3)"
     ```
     Or execute the full program:
     ```bash
     python3 solution/interpreter.py "fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;"
     ```