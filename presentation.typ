#set page(width: 20cm, height: 11cm)

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
          let hello = "Hello Booster!";
          let booster = "Booster!"
          print(+ hello booster)

          > Hello Booster!
          ```
        ]
      ]
      #colbreak()
      #box[
        ```rust
        let hello = "Hello Noria!";
        let noria = "Noria!"
        print(+ hello noria)

        > Hello Noria!
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

  We can split up our parsing, evaluation and execution to handle those individually.
]

#slide("Parsing Expressions (1)")[
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
#slide("Parsing Expressions (2)")[
  Basic types like `IntLit` are simple.
  #box[
    ```python
    class IntLit:
      value: int
    ```
  ]
  A parser for this could look something like this.
  #box[
    ```python
    def parse_int_lit(input: str) -> IntLit:
      # ...
    ```
  ]
  We could then use it as follows.
  #box[
    ```python
    > parse_int_lit("123")
    IntLit(123)
    ```
  ]
]

#slide("Parsing Expressions (3)")[
  The `FunCall` (function call) type is slightly more complex.

  We care about two things, the name of the function and a list of arguments.
  #box[
    ```python
    class FunCall:
      name: str
      args: list[Expression]
    ```
  ]
  We can then define a function to parse this as well.
  #box[
    ```python
    > parse_function_call("foo(1, true)")
    FunCall("foo", [IntLit(1), BoolLit(True)])
    ```
  ]
]

#slide("Parsing Expressions (4)")[
  In general, we want to implement smaller parses that can be combined into this.
  #box[
    ```python
    > parse_expression("add 3 foo(1, true)")
    BinOp(
      "add", # Operator
      IntLit(3), # Operand 1
      FunCall("foo", [IntLit(1), BoolLit(True)]) # Operand 2
    )
    ```
  ]
]

#slide("Evaluating Expressions")[
  Once we an expression, we can simplify it to a `Value`.
  #box[
    ```py
    type Value = int | str | bool | list[Value] | FunctionDefinition

    def eval_expr(e: Expression) -> Value
      # ...
    ```
  ]

  - Evaluating an expression like `BinOp("add", IntLit(2), Intlint(3))` should turn into `5`.
  - Evaluating a function call would run the function and evaluate to the return value.
  - We store variable values in a type we call the `Environment`.

  #box[
    ```python
    type Environment = list[dict[str, Value]] # For variable value lookup

    def eval_var(var: Variable, env: Environment) -> Value
      value = lookup_var(var.name, env)
    ```
  ]
]

#slide("Parsing Statements (1)")[
  Statements are operations with side-effects or control structures. Usually these are lines in your code.
  #box[
    ```python
    type Statement = Print | VarDef | Assignment | Block | If | While | FunDef | Return
    ```
  ]
  1. Print to print output: `print "Hello!";`
  2. Variable definitions: `let x = 10;`
  3. Assignment to update variables: `x = 20;`
  4. Blocks for grouping statements and creating scopes: `let x = 0; { let y = 2; }`
  5. If-statements for making decisions: `if my_bool { ... }`
  6. While-loops for iteration: `while my_bool { ... }`
  7. Function definitions: `fun fibonacci() { ... }`
  8. Return statements to exit or return values from functions: `return 10`
]

#slide("Parsing Statements (2)")[
  #box[
    ```python
    class Print:
      expr: Expression
    ```
  ]
  #box[
    ```python
    def parse_print(input: str) -> Print
      # ...
    ```
  ]
  #box[
    ```python
    > parse_print("print 5")
    Print(IntLit(5))
    ```
  ]
]

#slide("Parsing Statements (2)")[
  #box[
    ```python
    class While:
      condition: Expression
      block: Block
    ```
  ]
  #box[
    ```python
    def parse_while(input: str) -> While
      # ...
    ```
  ]
  #box[
    ```python
    > parse_while("while true { print(0); }")
    While(
      BoolLit(True),
      Block([
        Print(IntLit(0)
    ]))
    ```
  ]
]

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

#slide("Tasks")[]

#slide("Integers and Printing")[

]

#slide("Variables")[

]

#slide("If-statements")[

]

#slide("Assignment")[

]

#slide("While-loops")[

]

#slide("Function Definitions")[

]

#slide("Function Calls")[

]
