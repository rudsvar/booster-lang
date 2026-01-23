#set page(width: 20cm, height: 12cm)

#let slide(title, body) = [
  #block(breakable: false)[
    = #title
    #pad(top: 1em, body)
  ]
  #pagebreak()
]

#let inline(body, color: "#eeeeee") = [
  #block(fill: rgb(color), radius: 1em)[#body]
]

#let box(body, color: "#eeeeee") = [
  #block(fill: rgb(color), radius: 1em)[
    #pad(1em)[
      #body
    ]
  ]
]

#slide("Make a Programming Language!")[
  with Rudi Blaha Svartveit
  #pad(y: 3em)[
    #columns(2)[
      #strike[
        #box[
          ```rust
          $ let hello = "Hello Booster!";
          $ let booster = "Booster!"
          $ print(+ hello booster)
          Hello Booster!
          ```
        ]
      ]
      #colbreak()
      #box[
        ```rust
        $ let hello = "Hello Noria!";
        $ let noria = "Noria!"
        $ print(+ hello noria)
        Hello Noria!
        ```
      ]]
  ]
]

#slide("Where do we start?")[
  We need to turn a text into something our computer can run. We can do that with either
  #pad(y: 3em)[
    #columns(2)[
      (1) a compiler that translates it to machine code,
      #box(color: "#d1d1e8")[
        ```
        $ gcc hello.c -o hello
        $ ./hello
        Hello World!
        ```
      ]
      #colbreak()
      (2) or an interpreter that runs our code on the fly.
      #box(color: "#d1e8d5")[
        ```
        $ python hello.py
        Hello World!
        ```
      ]
    ]
  ]
  Since we can piggyback off another language, like Python, making an interpreter is easier.
]

#slide("Steps of Interpreting")[

  The first step is to *parse* the source code, turning it into a model we can work with.

  #box[
    ```python
    class Program:
      # ...

    def parse_program(input: str) -> Program:
      # ...
    ```
  ]

  Once we have parsed a program, we can *execute* it.

  #box[
    ```python
    def execute_program(program: Program):
      # ...
    ```
  ]
  A program consists of *expressions* and *statements*.

  We can split up parsing, evaluation and execution to handle those two individually.
]

#slide("Parsing Expressions")[
  An expression is something we can *evaluate* or *simplify* to a value, or commonly anything that can be on the right side of a variable definition like `var x = <some expression>`.

  Our `Expression` type looks like this. `Lit` is short for Literal, `Fun` for function, `BinOp` for binary operation.
  #box[
    ```python
    type Expression = IntLit | BoolLit | StrLit | ListLit | Variable | BinOp | FunCall
    #    Examples:    5        true      "hi!"    [1,2,3]   foo        1 + 2   foo(x)
    ```
  ]
  The literals are all hardcoded values we can write in a program.
  With literals, binary operations, and function calls, we can write more complex expressions.
  Note that in our parser, we'll be using prefix notation for binary operations since it's easier to parse.
  #box[
    ```python
    2 * foo(x) # Infix notation
    mul 2 foo(x) # Prefix notation with operator name
    ```
  ]
]
// #slide("Parsing Expressions (2)")[
//   Basic types like `IntLit` are simple.
//   #box[
//     ```python
//     class IntLit:
//       value: int
//     ```
//   ]
//   A parser for this could look something like this.
//   #box[
//     ```python
//     def parse_int_literal(input: str) -> IntLit:
//       # ...
//     ```
//   ]
//   We could then use it as follows.
//   #box[
//     ```python
//     > parse_int_literal("123")
//     IntLit(123)
//     ```
//   ]
// ]

// #slide("Parsing Expressions (3)")[
//   The `FunCall` (function call) type is slightly more complex.

//   We care about two things, the name of the function and a list of arguments.
//   #box[
//     ```python
//     class FunCall:
//       name: str
//       args: list[Expression]
//     ```
//   ]
//   We can then define a function to parse this as well.
//   #box[
//     ```python
//     > parse_function_call("foo(1, true)")
//     FunCall("foo", [IntLit(1), BoolLit(True)])
//     ```
//   ]
// ]

// #slide("Parsing Expressions (4)")[
//   In general, we want to implement smaller parses that can be combined into this.
//   #box[
//     ```python
//     > parse_expression("add 3 foo(1, true)")
//     BinOp(
//       "add", # Operator
//       IntLit(3), # Operand 1
//       FunCall("foo", [IntLit(1), BoolLit(True)]) # Operand 2
//     )
//     ```
//   ]
// ]

#slide("Evaluating Expressions")[
  Once we an expression, we can simplify it to a `Value`.
  #box[
    ```py
    type Value = int | str | bool | list[Value] | FunctionDefinition

    def eval_expr(e: Expression) -> Value
    ```
  ]

  - Evaluating an expression like `BinOp("add", IntLit(2), Intlint(3))` should turn into `5`.
  - A function call would evaluate to its return value.
  - We also need an `Environment` to store and look up variable values.

  #box[
    ```python
    # A list of maps from variable names to their values. One map per scope.
    type Environment = list[dict[str, Value]] # Example: [{'x': 3}]

    def eval_var(var: Variable, env: Environment) -> Value
      value = lookup_var(var.name, env)
    ```
  ]
]

#slide("Parsing Statements")[
  Statements are operations with side-effects or control structures. Usually these are lines in your code.
  #box[
    ```python
    type Statement = Shout | VarDef | Assignment | Block | If | While | FunDef | Return
    ```
  ]
  1. Print to print output: `shout "Hello!";`
  2. Variable definitions: `let x = 10;`
  3. Assignment to update variables: `x = 20;`
  4. Blocks for grouping statements and creating scopes: `let x = 0; { let y = 2; }`
  5. If-statements for making decisions: `if my_bool { ... }`
  6. While-loops for iteration: `while my_bool { ... }`
  7. Function definitions: `fun fibonacci() { ... }`
  8. Return statements to exit or return values from functions: `return 10`
]

// #slide("Parsing Statements (2)")[
//   #box[
//     ```python
//     class Print:
//       expr: Expression
//     ```
//   ]
//   #box[
//     ```python
//     def parse_print(input: str) -> Print
//       # ...
//     ```
//   ]
//   #box[
//     ```python
//     > parse_print("print 5")
//     Print(IntLit(5))
//     ```
//   ]
// ]

// #slide("Parsing Statements (2)")[
//   #box[
//     ```python
//     class While:
//       condition: Expression
//       block: Block
//     ```
//   ]
//   #box[
//     ```python
//     def parse_while(input: str) -> While
//       # ...
//     ```
//   ]
//   #box[
//     ```python
//     > parse_while("while true { print(0); }")
//     While(
//       BoolLit(True),
//       Block([
//         Print(IntLit(0)
//     ]))
//     ```
//   ]
// ]

#slide("Executing Statements")[
  Similarly to when we evaluate expressions, we'd like to implement *exec_statement*.

  #box[
    ```python
    # Top level exec function
    def exec_statement(statement: Statement, env: Env) -> While:
      # ...

    # Specifically for print-statements
    def exec_print(p: Print, env: Env):
      value = eval_expr(p.expr, env)
      print(str(value))

    # Alternative version of `Print` called `Shout`
    def exec_shout(p: Shout, env: Env):
      value = eval_expr(p.expr, env)
      print(str(value).upper())
    ```
  ]
]

#slide("Tasks")[

  If you clone `https://github.com/rudsvar/booster-lang` you'll find `README.md` and two main directories you need to care about, `solution` and `tasks`.
  These two are copies of each other, but the latter has function bodies replaced with `NotImplementedError`.

  Your tasks will consist of implementing functions for parsing, evaluating expressions, and executing statements.
  As you complete tasks, you can run the interpreter on increasingly complex programs.

  The first step will let you run this.

  #box[
    ```sh
    $ python3 solution/interpreter.py 'shout 1;'
    1
    ```
  ]
]

#slide("")[
  ... and at the end, you can run programs like this!
  #box[
    ```js
    fun fibonacci(x) {
        if eq x 0 {
          return 0;
        }
        if eq x 1 {
          return 1;
        }
        return add (call fibonacci(sub x 1)) (call fibonacci(sub x 2));
    }

    let x = call fibonacci(10);

    shout x;
    ```
  ]
]

#slide("Integers and Printing")[
  Our goal is to be able to run the following in our terminal.
  #footnote([The `$` represents a shell command to run, and the line below is output.])
  #box[
    ```sh
    $ python3 tasks/interpreter.py "shout 42;"
    42
    ```
  ]

  This program consists of a `shout` statement that will print the expression `42`, which in this case is just an integer literal.
  To run this program, we must implement the following functionality.

  - `parse_int`
  - `eval_int`
  - `parse_shout`
  - `exec_shout`

  See task 1 in `README.md` for more information.
]

#slide("Variables")[
  The next step is to be able to define and use variables.
  Instead of `let` you can name the keyword something else.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "let x = 10; shout x;"
    10
    ```
  ]

  Optionally, you can make a `$`-prefix mandatory for variables like `$x`.

  - `parse_var`
  - `parse_var_def`
  - `define_var`, `lookup_var`
  - `eval_var`
  - `exec_var_def`
]

#slide("Binary operations")[
  We need some way to make more complex expressions and computations.
  For that, we can use binary operations like addition and multiplication.
  You can use symbols or other names if you want.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "shout add 2 3;"
    5
    ```
  ]
  You can also combine it with variables.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "let x = 2; shout add x 3;"
    5
    ```
  ]

  - `parse_binary_operation`
  - `eval_binary_operation`
]

#slide("If-statements")[
  We can implement if-statements to make choices.
  You can name `if` something else, like `when`.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "if eq 2 2 { shout 1; }"
    1
    ```
  ]

  - Operator `eq` (equal).
  - `parse_if`
  - `exec_if`
]

#slide("Assignment")[
  We need to be able to modify variables after they have been defined.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "let x = 0; x = add x 1; shout x;"
    1
    ```
  ]

  - `parse_assignment`
  - `assign_var`
  - `exec_assignment`
]

#slide("While-loops")[
  To repeat code multiple times, we can use while loops.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "let x = 0; whilst neq x 10 { shout x; x = add x 1; }"
    0
    1
    2
    .
    .
    .
    9
    ```
  ]

  - Operator `neq` (not equal).
  - `parse_whilst`
  - `exec_whilst`
]

#slide("Function Definitions")[
  We can define our own functions to reuse code.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "fun double(x) { return add x x; }"
    ```
  ]

  - `parse_function_definition`
  - `exec_function_definition`
]

#slide("Function Calls")[
  To use functions, we need to be able to call them with arguments.
  #box[
    ```sh
    $ python3 tasks/interpreter.py "fun add(x, y) { return add x y; } let z = call add(2, 3); shout z;"
    5
    ```
  ]

  - `parse_function_call`
  - `eval_function_call`
]

= ???
