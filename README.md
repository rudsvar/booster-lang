# Booster Lang

A workshop to create a small interpreted language.
Tasks are further down.

## Suggested Setup

Install the following to get started quickly.

- Python 3.11+
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

0. **Familiarize yourself with the existing code**.
	Take a look at `statement.py`, `parser.py`, and `interpreter.py` and run the examples above to understand the structure of the program. 
	- **statement.py**: Defines a union type called `Statement` that represents all possible statements in the language.
	
		It also defines types for each statement and data they contain. For example, the `Print` statement has a field for the expression to print.

		`Expression` is another union type that can be either an integer literal or a variable name (string).
		To keep the language simple, we only allow these two by default.

	- **parser.py**: Parses source code into statements.

		`if __name__ == "__main__"` is the entry point for parsing. It reads the source code (either from a string argument or a file), then calls `parse_program` to convert it into a list of statements.
	
		``parse_program`` first splits the input by semicolons to get individual statements, then splits each statement by whitespace into tokens. For example, the input `print 42; let x 10` would be split into `['print 42', 'let x 10']`, and those are split into tokens like `['print', '42']` and `['let', 'x', '10']`.

		`parse_statement` will then match on the list on tokens to turn it into a `Statement` object. Your tasks will involve extending `parse_statement` to handle new statement types.

		`parse_expression` is a helper function that takes a token and determines if it's an integer literal or a variable name, returning the appropriate expression type.

	- **interpreter.py**: Executes statements and tracks the program state.

		The `Interpreter` needs some way of keeping track of state such as variables and their values, as well as the line we are executing. Not all of the fields are used immediately, but will become useful as we make progress.

		Like previously, `if __name__ == "__main__"` is the entry point for execution. It reads the source code, parses it into statements, initializes the `Interpreter` and then runs it.

		`__init__` initializes the interpreter's state by creating an empty environment (`env`) for variables, setting the `position` to 0, and so on. It also reads through the statement to find label and procedure statements that we'll need later.

		`execute_program` continues executing statements until we reach the end of the program. It calls `execute_statement` on the current statement and increments the position.

		`execute_statement` takes a statement and performs the appropriate action based on its type. For example, if it's a `Print` statement, it evaluates the expression to print and prints it.
		Your tasks will involve extending `execute_statement` to handle new statement types and update the interpreter's state accordingly.

		`eval_expr` is a helper function that takes an expression and evaluates it to a value. For integer literals, it returns the integer. For variable names, it looks up the variable in the environment and returns its value.

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
	You can turn the second token into an `Expression` with `parse_expression`, which will handle both integer literals and variable names.
	  
	  ```
	  $ python3 parser.py "print 42;"
	  [Print(expr=42)]
	  $ python3 parser.py "print x;"
	  [Print(expr='x')]
	  ```

	- **interpreter.py**: Add a case for `Print(expr)` in `execute_statement` that evaluates the expression and prints the result.
	  
	  ```
	  $ python3 interpreter.py "print 42;"
	  42
	  $ python3 interpreter.py "print x;"
	  Undefined variable: 'x'
	  ```

3. **Let**


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
