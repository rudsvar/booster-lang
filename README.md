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
python3 interpreter.py "set x 5; print x;"
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
python3 parser.py --debug "print 42;"
python3 interpreter.py --debug "set x 5; print x"
```

## Tasks

Follow the statement order in [parser.py](parser.py). Each task has a parser change and a matching interpreter change.

1. **Skip**
	- Parser: accept an empty list of tokens and return `Skip()`.
	- Interpreter: do nothing; this is a no-op statement. Use `pass` in the case block.
	- Parser example: `python3 parser.py ";"`
	- Interpreter example: `python3 interpreter.py ";"`
2. **Print**
	- Parser: `print <expr>` to `Print`.
	- Interpreter: evaluate the expression using `eval()`, then print the result to stdout.
	- Parser example: `python3 parser.py "print 42;"`
	- Interpreter example: `python3 interpreter.py "print 42;"`
3. **VarDef**
	- Parser: `set <name> <expr>` to `VarDef`.
	- Interpreter: evaluate the expression and store the result in the `env` dict under the given name. Create or overwrite the variable.
	- Parser example: `python3 parser.py "set x 5;"`
	- Interpreter example: `python3 interpreter.py "set x 5; print x;"`
4. **Inc**
	- Parser: `inc <name> <expr>` to `Inc`.
	- Interpreter: add the evaluated expression to the variable's current value. The variable must already exist in `env`.
	- Parser example: `python3 parser.py "inc x 2;"`
	- Interpreter example: `python3 interpreter.py "set x 1; inc x 2; print x;"`
5. **Dec**
	- Parser: `dec <name> <expr>` to `Dec`.
	- Interpreter: subtract the evaluated expression from the variable's current value. The variable must already exist in `env`.
	- Parser example: `python3 parser.py "dec x 2;"`
	- Interpreter example: `python3 interpreter.py "set x 5; dec x 2; print x;"`
6. **Mul**
	- Parser: `mul <name> <expr>` to `Mul`.
	- Interpreter: multiply the variable's current value by the evaluated expression. The variable must already exist in `env`.
	- Parser example: `python3 parser.py "mul x 7;"`
	- Interpreter example: `python3 interpreter.py "set x 6; mul x 7; print x;"`
7. **Swap**
	- Parser: `swap <left> <right>` to `Swap`.
	- Interpreter: exchange the values of the two variables in `env`. Both must already exist. Hint: use Python tuple unpacking: `self.env[left], self.env[right] = self.env[right], self.env[left]`.
	- Parser example: `python3 parser.py "swap a b;"`
	- Interpreter example: `python3 interpreter.py "set a 1; set b 2; swap a b; print a; print b;"`
8. **Label**
	- Parser: `label <name>` to `Label`.
	- Interpreter: pre-process during initialization (in `__init__`) to map label names to their statement positions. During execution, labels themselves are no-ops. Hint: use `pass` in the case block.
	- Parser example: `python3 parser.py "label start;"`
	- Interpreter example: `python3 interpreter.py "label start; print 1;"`
9. **Goto**
	- Parser: `goto <label>` to `Goto`.
	- Interpreter: set the position to the instruction index of the labeled statement. Use the pre-computed `labels` dict from initialization.
	- Parser example: `python3 parser.py "goto end;"`
	- Interpreter example: `python3 interpreter.py "goto end; print 1; label end; print 2;"`
10. **If**
	- Parser: `if <left> <op> <right> then <statement>` to `If`.
	- Interpreter: evaluate both sides, apply the operator (==, <, >, <=, >=, !=), and execute the nested statement only if the condition is true. Hint: use a dict to map operators to boolean expressions for clean code.
	- Parser example: `python3 parser.py "if 2 < 3 then print 1;"`
	- Interpreter example: `python3 interpreter.py "if 2 < 3 then print 1;"`
11. **Exit**
	- Parser: `exit` to `Exit`.
	- Interpreter: stop the program immediately by setting `position` to the end of the program (skip remaining statements).
	- Parser example: `python3 parser.py "exit;"`
	- Interpreter example: `python3 interpreter.py "print 1; exit; print 2;"`
12. **Proc**
	- Parser: `proc <name> <param...>` to `Proc`.
	- Interpreter: pre-process during initialization to map procedure names to their `Proc` statement and statement position. During execution, procedures are no-ops (the definition is already recorded). Hint: use `pass` in the case block.
	- Parser example: `python3 parser.py "proc noop;"`
	- Interpreter example: `python3 interpreter.py "proc noop; return;"`
13. **Call**
	- Parser: `call <name> <arg...>` to `Call`.
	- Interpreter: push the current position onto the call stack, bind each argument to the corresponding parameter as a variable in `env`, and jump to the procedure's statement position. Hint: use `zip(proc.params, args)` to pair parameters with arguments.
	- Parser example: `python3 parser.py "call add 2 3;"`
	- Interpreter example: `python3 interpreter.py "proc add a b; set result a; inc result b; return; call add 2 3; print result;"`
14. **Return**
	- Parser: `return` to `Return`.
	- Interpreter: pop the return address from the call stack and set `position` to that saved location, resuming execution after the call.
	- Parser example: `python3 parser.py "return;"`
	- Interpreter example: `python3 interpreter.py "proc one; set result 1; return; call one; print result;"`

## Glossary

- **Program**: A sequence of statements separated by semicolons, as a string or file.
- **Statement**: A single instruction in the language (e.g., `print`, `set`, `if`, etc.). Defined as a union type in `statement.py`.
- **Expression**: A value that can be evaluated: either a literal integer (e.g., `42`) or a variable name (e.g., `x`). Type is `int | str`.
- **Value**: The result of evaluating an expression; always an integer in this language.
- **Eval**: Evaluate an expression to a value (see `eval()` method in the interpreter).
- **Exec**: Execute a statement, which may have side effects (see `execute()` method in the interpreter).
- **Parse**: Convert source code (string) into a list of statements (AST).
- **AST**: Abstract Syntax Tree; the in-memory representation of the program as statement objects.
- **Env**: The environment dict (also called a map in other languages) (`env`) storing all variable bindings.
- **Position**: The current instruction index during execution (`position` in the interpreter).
- **Label**: A named marker in the code used for jumps.
- **Goto**: Jump to a labeled statement.
- **Proc**: A named procedure (like a function, but note: procedures don't return values directly; they communicate results via the global `result` variable).
- **Call**: Invoke a procedure by name with arguments.
- **Stack**: The call stack (`stack`) storing return addresses for procedure calls.
