# Booster Lang

There are six main parts to the solution directory:

- **BaseParser** pre-implements low-level parsing functions.
- **Expression Parser** for parsing expressions and defining types to parse them into.
- **Statement Parser** for parsing statements and defining types to parse them into.
- **Expression Evaluator** for evaluating expressions to values.
- **Statement Executor** for executing statements with side effects.
- **Interpreter** for parsing and running complete programs.

## BaseParser

BaseParser provides low-level parsing functions. Use this as a reference for implementing the higher-level parsers.

### Character and String Parsing

| Function | Description |
|----------|-------------|
| .parse_digits() | Parse one or more digits (0-9). |
| .parse_identifier() | Parse a valid identifier (letters, numbers, underscores). |
| .parse_string(target) | Parse an exact string and consume it. |
| .parse_until(target) | Parse characters until target is reached without consuming target. |

### Keyword and Symbol Parsing

| Function | Description |
|----------|-------------|
| .parse_keyword(keyword) | Parse a keyword followed by optional whitespace, fails if followed by alphanumerics. |
| .parse_symbol(target) | Parse a symbol like "{", "}", "(", ")" followed by optional whitespace. |
| .parse_constant(constants) | Parse a constant string like "true" or "false". |
| .parse_one_of_constants(constants) | Try to parse one of several constants. |

### Whitespace

| Function | Description |
|----------|-------------|
| .parse_whitespace() | Consume and discard all whitespace (spaces, tabs, newlines). |

### Combinators

| Function | Description |
|----------|-------------|
| .any(parsers) | Try each parser in order until one succeeds. |
| .optional(parser) | Try to parse something, returning None if it fails without consuming input. |
| .zero_or_more(parser) | Run a parser zero or more times and return a list of results. |
| .separated_by(parser, separator) | Parse items separated by a separator like comma-separated lists. |

### Notes

- Once you parse something, it's removed from the input automatically.
- Some functions like .parse_symbol() and .parse_keyword() automatically consume trailing whitespace.
- Use .any() to try multiple alternatives. We commit to the one that first consumes some input, and will not try any others afterwards.

## Running Parsers and the Interpreter

Each of the other parsers can be run directly from the command line.
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

### Expression Evaluator
Evaluate a single expression:
```bash
python3 solution/expression_evaluator.py "42"
python3 solution/expression_evaluator.py "add 2 3"
python3 solution/expression_evaluator.py "[1, 2, 3]"
python3 solution/expression_evaluator.py 'add "hello" " world"'
python3 solution/expression_evaluator.py "add [1, 2] [3, 4]"
```

### Statement Executor
Execute a single statement:
```bash
python3 solution/statement_executor.py "let x = 5;"
python3 solution/statement_executor.py "shout x;"
python3 solution/statement_executor.py "if true { let y = 10; shout y; }"
```

### Interpreter
Parse and execute a program:
```bash
python3 solution/interpreter.py examples/fibonacci.blang
python3 solution/interpreter.py "let x = 5; shout x;"
```

## Tasks

The tasks will mostly switch between the five main parts to continuously extend the language as you implement it.
You will implement predefined functions in the expression parser, expression evaluator, statement parser, and statement executor to extend the interpreter.

In any of the following tasks, you can rename keywords, switch out symbols, or change the behavior, as long as it don't cause ambiguity for the parser.
Just remember to modify the test commands accordingly.
For example, instead of `print`, the example solution has the `shout` keyword that prints a stringified uppercase version of the input.

1. **Print integers and basic types**
   
   Run: `python3 tasks/interpreter.py "shout 42;"`
   
   - Implement `parse_int` and test with `python3 tasks/expression_parser.py "42"`
   - Implement `eval_int` and test with `python3 tasks/expression_evaluator.py "42"`
   - Implement `parse_shout` and test with `python3 tasks/statement_parser.py "shout 42;"`
   - Implement `exec_shout` and run `python3 tasks/interpreter.py "shout 42;"`
   - Optional: Implement `parse_bool_literal` and `eval_bool` and test with `python3 tasks/expression_evaluator.py "true"`
   - Optional: Implement `parse_string_literal` and `eval_string` and test with `python3 tasks/expression_evaluator.py '"Hello World!"'`

2. **Variable definitions and lookups**
   
   Run: `python3 tasks/interpreter.py "let x = 10; shout x;"`
   
   - Implement `parse_var` and test with `python3 tasks/expression_parser.py "x"`
   - Implement `parse_var_def` and test with `python3 tasks/statement_parser.py "let x = 10;"`
   - Implement `define_var`, `lookup_var`, `eval_var`, and `exec_var_def` and run `python3 tasks/interpreter.py "let x = 10; shout x;"`

3. **Binary operations**
   
   Run: `python3 tasks/interpreter.py "shout add 2 3;"`
   
   - Implement `parse_binary_operation` and test with `python3 tasks/expression_parser.py "add 2 3"`
   - Implement `eval_binary_operation` and run `python3 tasks/expression_evaluator.py "add 2 3"`
   - Or execute with `python3 tasks/interpreter.py "shout add 2 3;"`
   - Optional: Add more operators such as `<` (less than).

4. **Blocks and scoping**
   
   Run: `python3 tasks/interpreter.py "let x = 10; { let y = 20; shout x; }"`
   
   - Implement `parse_block` and test with `python3 tasks/statement_parser.py "{ let x = 10; shout x; }"`
   - Implement `exec_block` and run `python3 tasks/interpreter.py "{ let x = 10; shout x; }"`

5. **Conditionals**
   
   Run: `python3 tasks/interpreter.py "if eq 2 2 { shout eq 3 4; }"`
   
   - Implement the operator `eq` or `==` that checks if two values are equal and test with `python3 tasks/expression_evaluator.py "eq 2 2"`
   - Implement `parse_if` and test with `python3 tasks/statement_parser.py "if eq 2 3 { shout \"True!\"; }"`
   - Implement `exec_if` and run `python3 tasks/interpreter.py "if eq 2 3 { shout \"True!\"; }"`
   - Optional: Implement parsing an optional `else`-block after the if.

6. **Loops and variable assignment**
   
   Run: `python3 tasks/interpreter.py "let x = 0; whilst neq x 10 { shout x; x = add x 1; }"`
   
   - Implement the operator `neq` or `!=` that checks if two values inequal and test with `python3 tasks/expression_evaluator.py "neq 2 3"`
   - Implement `parse_assignment` and test with `python3 tasks/statement_parser.py "x = add x 1;"`
   - Implement `assign_var` and `exec_assignment` and test with `python3 tasks/interpreter.py "let x = 0; x = add x 1; shout x;"`
   - Implement `parse_whilst` and test with `python3 tasks/statement_parser.py "whilst neq x 10 { shout x; }"`
   - Implement `exec_whilst` and test with `python3 tasks/interpreter.py "let x = 0; whilst neq x 10 { shout x; x = add x 1; }"`

7. **Functions**
   
   Run: `python3 tasks/interpreter.py "fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;"`
   
   - Implement `parse_function_call` and test with `python3 tasks/expression_parser.py "call add(2, 3)"`
   - Implement `parse_function_definition` and test with `python3 tasks/statement_parser.py "fun add(x, y) { return x y; }"`
   - Implement `eval_function_call`, `exec_function_definition` and run `python3 tasks/expression_evaluator.py "call add(2, 3)"`
   - Or execute the full program `python3 tasks/interpreter.py "fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;"`