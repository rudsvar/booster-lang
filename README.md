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
	- Interpreter: do nothing.
	- Parser example: `python3 parser.py ";"`
	- Interpreter example: `python3 interpreter.py ";"`
2. **Print**
	- Parser: `print <expr>` to `Print`.
	- Interpreter: evaluate and print the expression.
	- Parser example: `python3 parser.py "print 42;"`
	- Interpreter example: `python3 interpreter.py "print 42;"`
3. **VarDef**
	- Parser: `set <name> <expr>` to `VarDef`.
	- Interpreter: assign in `env`.
	- Parser example: `python3 parser.py "set x 5;"`
	- Interpreter example: `python3 interpreter.py "set x 5; print x;"`
4. **Inc**
	- Parser: `inc <name> <expr>` to `Inc`.
	- Interpreter: add evaluated value.
	- Parser example: `python3 parser.py "inc x 2;"`
	- Interpreter example: `python3 interpreter.py "set x 1; inc x 2; print x;"`
5. **Dec**
	- Parser: `dec <name> <expr>` to `Dec`.
	- Interpreter: subtract evaluated value.
	- Parser example: `python3 parser.py "dec x 2;"`
	- Interpreter example: `python3 interpreter.py "set x 5; dec x 2; print x;"`
6. **Mul**
	- Parser: `mul <name> <expr>` to `Mul`.
	- Interpreter: multiply by evaluated value.
	- Parser example: `python3 parser.py "mul x 7;"`
	- Interpreter example: `python3 interpreter.py "set x 6; mul x 7; print x;"`
7. **Swap**
	- Parser: `swap <left> <right>` to `Swap`.
	- Interpreter: exchange values.
	- Parser example: `python3 parser.py "swap a b;"`
	- Interpreter example: `python3 interpreter.py "set a 1; set b 2; swap a b; print a; print b;"`
8. **Label**
	- Parser: `label <name>` to `Label`.
	- Interpreter: record labels at startup.
	- Parser example: `python3 parser.py "label start;"`
	- Interpreter example: `python3 interpreter.py "label start; print 1;"`
9. **Goto**
	- Parser: `goto <label>` to `Goto`.
	- Interpreter: jump to label position.
	- Parser example: `python3 parser.py "goto end;"`
	- Interpreter example: `python3 interpreter.py "goto end; print 1; label end; print 2;"`
10. **If**
	- Parser: `if <left> <op> <right> then <statement>` to `If`.
	- Interpreter: execute statement when condition is true.
	- Parser example: `python3 parser.py "if 2 < 3 then print 1;"`
	- Interpreter example: `python3 interpreter.py "if 2 < 3 then print 1;"`
11. **Exit**
	- Parser: `exit` to `Exit`.
	- Interpreter: stop execution.
	- Parser example: `python3 parser.py "exit;"`
	- Interpreter example: `python3 interpreter.py "print 1; exit; print 2;"`
12. **Proc**
	- Parser: `proc <name> <param...>` to `Proc`.
	- Interpreter: record procedures at startup.
	- Parser example: `python3 parser.py "proc noop;"`
	- Interpreter example: `python3 interpreter.py "proc noop; return;"`
13. **Call**
	- Parser: `call <name> <arg...>` to `Call`.
	- Interpreter: set args, jump into procedure.
	- Parser example: `python3 parser.py "call add 2 3;"`
	- Interpreter example: `python3 interpreter.py "proc add a b; set result a; inc result b; return; call add 2 3; print result;"`
14. **Return**
	- Parser: `return` to `Return`.
	- Interpreter: pop return address and jump back.
	- Parser example: `python3 parser.py "return;"`
	- Interpreter example: `python3 interpreter.py "proc one; set result 1; return; call one; print result;"`
