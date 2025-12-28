#set page(width: 25cm, height: 14cm)

#let slide(title, body) = [
  #block(breakable: false)[
    = #title
    #pad(top: 1em, body)
  ]
  #pagebreak()
]

#let box(body) = [
  #block(fill: rgb("#eeeeee"), radius: 1em)[
    #pad(1em)[
      #body
    ]
  ]
]

#slide("Make a Programming Language")[
  with Rudi Blaha Svartveit
  #pad(x: 1em)[]
  ```rust
  let hello = "Hello Booster!";
  let booster = "Booster!"
  print(+ hello booster)

  > Hello Booster!
  ```
]

#slide("Program")[
  - 09:00 - 10:30: Part 1

    - 09:00: Introduction to parsing and interpreting
    - 09:30: Parsing and evaluating expressions
    - 10:00: Parsing and executing statements

  - 10:30 - 10:50: Break

  - 10:50 - 12:20: Part 2

    - 10:50: Interpreting a program
    - 11:20: Implementing more advanced control structures
    - 11:50: Making your own language constructs
]

#slide("Parsing")[
  Parsing is about making data more structured.

  #box[
    ```python
    def parse_int(s: str) -> int:
      return int(s)

    int_text = "123"

    i: int = parse_int(input)

    print(i + 2)
    ```
  ]

  If it's a valid integer, we can then perform more specific operations on it like addition.
]

#slide("Parsing a whole program")[
  We can make it a lot more complex.

  #box[
    ```python
    def parse_program(program_text: str) -> Program
      ...

    program_text: str = """
      let x = 0;
      while x < 10 {
      x = x + 1;
      }
      print(x);
    """

    program: Program = parse_program(program_text)
    ```
  ]
]

#slide("Interpreters vs Compilers")[
  The source code of a program is just text, and cannot be run on its own.
  We require another program that can translate it to something the computer can run.

  1. Compilers parse the program source code and turns the result into executable machine code.
    When the compiler completes that task, its task is done.
    The end result can be executed directly.
    #box[
      ```bash
      $ gcc helloworld.c -o helloworld # Turn helloworld.c into an executable file
      $ ./helloworld # Run the executable file
      Hello world! # Program output
      ```
    ]
  2. Interpreters still have to parse the source code to be able to work with it, but can then perform the work that the source code specified on its behalf.
    #box[
      ```bash
      $ python helloworld.py
      Hello world!
      ```
    ]
]

#slide("Implementing a parser")[

  We have to define some types to parse program text into

  #box[
    ```python
    type Expr = int
    type Statement = VariableDeclaration | Print
    type Program = list[Statement]
    ```
  ]

  Then define functions that turn the program text into them

  #box[
    ```python
    def parse_int(input: str) -> Program:
      ...

    def parse_expression(input: str) -> Program:
      ...

    def parse_statement(input: str) -> Program:
      ...

    def parse_program(input: str) -> Program:
      ...
    ```
  ]
]

#slide("Keeping track of state")[
  ```python
  def parse_program(input: Input) -> Program:
    ...
  ```
]

#slide("Implementing an interpreter")[
  #box[
    ```python
    def run_program(program: Program):
      ...

    program_text: str = "let x = 10; print(x);"
    program: Program = parse_program(program_text)
    run_program(program) # Run the interpreter
    ```
  ]

  The output of running
]

#slide("Python Features")[
  1. Type annotations and strict type checking
    #box[
      ```python
      i: int = 10
      s: str = "Hi!"
      f: float = "Uh oh"
      ```
    ]
  2. Data classes
    #box[
      ```python
      @dataclass
      class VarDecl:
        name: str
        value: Expr
      ```
    ]
  3. Union types
    #box[
      ```python
      type Expr = int | str | bool
      type Statement = VarDecl | Print
      ```
    ]
]
