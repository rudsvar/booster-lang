# Booster Lang

A workshop to create a small interpreted language.
Tasks are further down.

## Suggested Setup

Install the following to get started quickly.

- **Python 3.10+** (required for pattern matching and union type syntax)
- Visual Studio Code
- The `Python` extension
- The `Black Formatter` extension

## Overview

- [statement.py](statement.py): Statement and expression definitions.
- [parser.py](parser.py): Parses source into statements; splits by semicolon then whitespace.
- [interpreter.py](interpreter.py): Executes statements with a single global environment.
- [parser_tests.py](parser_tests.py): Unit tests for parsing.
- [interpreter_tests.py](interpreter_tests.py): Unit tests for execution.
- [examples/](examples/): Sample programs used by tests.

## Examples

Parse or run a short program:

```bash
python3 parser.py "print 42;"
python3 interpreter.py "print 42;"
```

Parse or run a program from a file:

```bash
python3 parser.py examples/fibonacci.blang
python3 interpreter.py examples/fibonacci.blang
```

Get usage information:

```
python3 parser.py --help
python3 interpreter.py --help
```

Enable debug logs:

```bash
python3 parser.py "print 42;" --debug
python3 interpreter.py "print 42;" --debug
```

## Tasks

Follow the statement order in [parser.py](parser.py). Each task has a parser change and a matching interpreter change.

0. **Run the tests to see what needs to be done**.

	In Visual Studio Code, open the Testing panel (click the beaker icon in the left sidebar). You should see the tests for `1_parser_tests.py` and `2_interpreter_tests.py`.

	Run all tests by clicking the play button at the top of the Testing panel. You'll see which tests are failing. Each failing test corresponds to a task below that needs to be implemented.

	As you complete each task, re-run the tests to see your progress. When all tests pass, you're done!

	**Tip**: You can also run tests from the command line:
	```bash
	python3 parser_tests.py
	python3 interpreter_tests.py
	```

1. **Skip**: The simplest statement we can add is a `skip` statement that does nothing.

	- **parser.py**: Add a match case for an empty list of tokens in `parse_statement` that returns a `Skip()` statement object.

	  ```
	  $ python3 parser.py ""
	  [Skip()]
	  ```
	- **interpreter.py**: Add a case for `Skip` in `execute_statement` that does nothing.
	  You can do nothing in a match statement by using `pass` in Python.
	  You should be able to run `python3 interpreter.py ""` and see that it executes without errors and produces no output.

	  ```
	  $ python3 interpreter.py ""
	  (no output)
	  ```

2. **Print**: The `print` statement lets us produce output from our program.

	- **parser.py**: Add a case for `print` in `parse_statement` that expects the keyword `print` followed by an expression (either an integer literal or a variable name). It should return a `Print` statement object containing the expression.
	You can turn the second token into an `Expression` with `parse_expr`, which will handle both integer literals and variable names.

	  ```
	  $ python3 parser.py "print 42;"
	  [Print(expr=42)]
	  $ python3 parser.py "print x;"
	  [Print(expr='x')]
	  ```

	- **interpreter.py**: Add a case for `Print(expr)` in `execute_statement` that evaluates the expression with `eval_expr` and prints the result.

	  ```
	  $ python3 interpreter.py "print 42;"
	  42
	  $ python3 interpreter.py "print x;"
	  Undefined variable: 'x'
	  ```

3. **Let**: The `let` statement allows us to create variables and assign values to them.

	- **parser.py**: Add a case for `let` in `parse_statement` that expects the keyword `let` followed by a variable name and an expression. It should return a `Let` statement object containing the variable name and the expression.

	  ```
	  $ python3 parser.py "let x 10;"
	  [Let(var='x', expr=10)]
	  $ python3 parser.py "let y x;"
	  [Let(var='y', expr='x')]
	  ```

	- **interpreter.py**: Add a case for `Let(var, expr)` in `execute_statement` that evaluates the expression and stores the result in the environment under the given variable name.

	  ```
	  $ python3 interpreter.py "let x 10; print x;"
	  10
	  $ python3 interpreter.py "let y x; print y;"
	  Undefined variable: 'x'
	  ```

4. **Inc**: The `inc` statement lets us increment the value of an existing variable by a specified amount.

	- **parser.py**: Add a case for `inc` in `parse_statement` that expects the keyword `inc` followed by a variable name and an expression. It should return an `Inc` statement object containing the variable name and the expression.

	  ```
	  $ python3 parser.py "inc x 5;"
	  [Inc(var='x', expr=5)]
	  $ python3 parser.py "inc y x;"
	  [Inc(var='y', expr='x')]
	  ```

	- **interpreter.py**: Add a case for `Inc(var, expr)` in `execute_statement` that evaluates the expression, retrieves the current value of the variable from the environment, adds them together, and stores the result back in the environment under the same variable name.

	  ```
	  $ python3 interpreter.py "let x 10; inc x 5; print x;"
	  15
	  $ python3 interpreter.py "let y 20; inc y x; print y;"
	  Undefined variable: 'x'
	  ```

5. Optional: **Dec**, **Mul**, or other operations. Like `inc`, you can add statements for decrementing a variable (`dec`), multiplying a variable by an expression (`mul`), or any other operation you can think of. The process is the same: add a case in the parser to create the appropriate statement object, and add a case in the interpreter to evaluate it and update the environment.

6. **Swap**: A `swap` statement that takes two variable names and swaps their values in the environment.

	- **parser.py**: Add a case for `swap` in `parse_statement` that expects the keyword `swap` followed by two variable names. It should return a `Swap` statement object containing the two variable names.

	  ```
	  $ python3 parser.py "swap x y;"
	  [Swap(var1='x', var2='y')]
	  ```

	- **interpreter.py**: Add a case for `Swap(var1, var2)` in `execute_statement` that retrieves the current values of both variables from the environment, swaps them, and stores the results back in the environment under their respective variable names.

	  ```
	  $ python3 interpreter.py "let x 10; let y 20; swap x y; print x; print y;"
	  20
	  10
	  ```

7. **Label**: Labels mark positions in the code that can be jumped to with `goto`.

	- **parser.py**: Add a case for `label` in `parse_statement` that expects the keyword `label` followed by a label name. It should return a `Label` statement object containing the label name.

	  ```
	  $ python3 parser.py "label loop;"
	  [Label(name='loop')]
	  ```

	- **interpreter.py**: Add a case for `Label(name)` in `execute_statement` that does nothing (use `pass`). Labels are processed during initialization in `__init__` to build the `labels` dict mapping label names to positions.

	  ```
	  $ python3 interpreter.py "label start;" --debug
	  (You'll see the Label statement being executed in the debug output)
	  ```

8. **Goto**: The `goto` statement jumps to a labeled position in the code.

	- **parser.py**: Add a case for `goto` in `parse_statement` that expects the keyword `goto` followed by a label name. It should return a `Goto` statement object containing the label name.

	  ```
	  $ python3 parser.py "goto end;"
	  [Goto(label='end')]
	  ```

	- **interpreter.py**: Add a case for `Goto(label)` in `execute_statement` that sets `self.position` to the position of the label (looked up in `self.labels`).

	  ```
	  $ python3 interpreter.py "goto end; print 1; label end; print 2;"
	  2
	  (skips printing 1)

	  $ python3 interpreter.py "let x 0; label loop; print x; inc x 1; goto loop;"
	  0
	  1
	  2
	  ...
	  (infinite loop - press Ctrl+C to stop)
	  ```

9. **If**: The `if` statement conditionally executes a statement based on a comparison.

	- **parser.py**: Add a case for `if` in `parse_statement` that expects the pattern `if <expr> <operator> <expr> then <statement>`. It should return an `If` statement object containing the left expression, operator, right expression, and the statement to execute if the condition is true.

	  ```
	  $ python3 parser.py "if 5 > 3 then print 1;"
	  [If(left=5, operator='>', right=3, statement=Print(expr=1))]
	  ```

	- **interpreter.py**: Add a case for `If(left, operator, right, statement)` in `execute_statement` that evaluates both expressions, applies the comparison operator (==, <, >, <=, >=, !=), and executes the nested statement if the condition is true.

	  ```
	  $ python3 interpreter.py "if 5 > 3 then print 1;"
	  1
	  $ python3 interpreter.py "if 2 > 3 then print 1;"
	  (no output)
	  ```

10. **Exit**: The `exit` statement terminates the program immediately.

	- **parser.py**: Add a case for `exit` in `parse_statement` that expects just the keyword `exit`. It should return an `Exit` statement object.

	  ```
	  $ python3 parser.py "exit;"
	  [Exit()]
	  ```

	- **interpreter.py**: Add a case for `Exit()` in `execute_statement` that sets `self.position` to the length of the program, effectively ending execution.

	  ```
	  $ python3 interpreter.py "print 1; exit; print 2;"
	  1
	  (exits before printing 2)
	  ```

11. **Proc**: Procedures are reusable blocks of code with parameters.

	- **parser.py**: Add a case for `proc` in `parse_statement` that expects the keyword `proc` followed by a procedure name and zero or more parameter names. It should return a `Proc` statement object containing the procedure name and list of parameters.

	  ```
	  $ python3 parser.py "proc add a b;"
	  [Proc(name='add', params=['a', 'b'])]
	  ```

	- **interpreter.py**: Add a case for `Proc(name, params)` in `execute_statement` that does nothing (use `pass`). Procedures are processed during initialization in `__init__` to build the `procedures` dict.

	  ```
	  $ python3 interpreter.py "proc add a b;" --debug
	  (You'll see the Proc statement being executed in the debug output)
	  ```

12. **Call**: The `call` statement invokes a procedure with arguments.

	- **parser.py**: Add a case for `call` in `parse_statement` that expects the keyword `call` followed by a procedure name and zero or more argument expressions. It should return a `Call` statement object containing the procedure name and list of arguments.

	  ```
	  $ python3 parser.py "call add 3 5;"
	  [Call(name='add', args=[3, 5])]
	  ```

	- **interpreter.py**: Add a case for `Call(name, args)` in `execute_statement` that:
	  1. Pushes the current position onto the call stack
	  2. Looks up the procedure in `self.procedures` to get its position
	  3. Sets `self.position` to the procedure's position
	  4. Evaluates each argument and binds it to the corresponding parameter in the environment

	  ```
	  $ python3 interpreter.py "goto main; proc add a b; let result a; inc result b; return; label main; call add 3 5; print result;"
	  8
	  ```

13. **Return**: The `return` statement exits a procedure and returns to the caller.

	- **parser.py**: Add a case for `return` in `parse_statement` that expects just the keyword `return`. It should return a `Return` statement object.

	  ```
	  $ python3 parser.py "return;"
	  [Return()]
	  ```

	- **interpreter.py**: Add a case for `Return()` in `execute_statement` that pops a position from the call stack and sets `self.position` to that value, returning control to the caller.

	  ```
	  $ python3 interpreter.py "goto main; proc greet; print 42; return; label main; call greet; print 99;"
	  42
	  99
	  ```

## Glossary

- **Program**: A sequence of statements separated by semicolons, as a string or file.
- **Statement**: A single instruction in the language (e.g., `print`, `set`, `if`, etc.). Defined as a union type in `statement.py`.
- **Expression**: A value that can be evaluated: either a literal integer (e.g., `42`) or a variable name (e.g., `x`). Type is `int | str`.
- **Value**: The result of evaluating an expression; always an integer in this language.
- **Eval**: Evaluate an expression to a value (see `eval_expr()` method in the interpreter).
- **Exec**: Execute a statement, which may have side effects (see `execute_statement()` method in the interpreter).
- **Parse**: Convert source code (string) into a list of statements (AST).
- **AST**: Abstract Syntax Tree; the in-memory representation of the program as statement objects.
- **Env**: The environment dict (also called a map in other languages) (`env`) storing all variable bindings.
- **Position**: The current instruction index during execution (`position` in the interpreter).
- **Label**: A named marker in the code used for jumps.
- **Goto**: Jump to a labeled statement.
- **Proc**: A procedure, like a function but only with side effects and no return value.
- **Call**: Invoke a procedure by name with arguments.
- **Stack**: The call stack (`stack`) storing return addresses for procedure calls.
