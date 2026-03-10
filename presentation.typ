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
    #box[
      ```rust
      $ let hello = "Hello Booster!";
      $ let booster = "Booster!"
      $ print(+ hello booster)
      Hello Booster!
      ```
    ]
  ]
  #pad(y: 1em)[
    1. Install Python: https://www.python.org/downloads/
    2. Install Visual Studio Code: https://code.visualstudio.com/
    3. Install the Python plugin
    4. Clone https://github.com/rudsvar/booster-lang
  ]
]

#slide("Where do we start?")[
  We need to make a program that can run another program.
  #pad(y: 3em)[
    #columns(2)[
      Just like Python's interpreter can run Python programs ...
      #box(color: "#d1e8d5")[
        ```
        $ python hello.py
        Hello World!
        ```
      ]
      #colbreak()
      ... we can make our own interpreter *in Python* to run our own programs.
      #box(color: "#d1e8f5")[
        ```
        $ python interpreter.py ten.blang
        10
        ```
      ]
    ]
  ]
  We use Python as a *host language* to make our own.
]

#slide("Interpreting in three steps")[

  We start by defining some classes to represent our program.

  #box[
    ```python
    class Program:
      statements: list[Statement]
    ```
  ]

  We then *parse* the source code, turning it into a model we can work with.

  #box[
    ```python
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
]

#slide("What will our language look like?")[

  To keep it simple enough for a workshop, we're keeping the syntax and functionality fairly limited.

  #pad(y: 3em)[
    #columns(2)[
      If we run `countdown.blang` ...
      #box(color: "#ffdddd")[
        ```
        let n 5;

        label countdown;
          print n;
          dec n 1;
          if n > 0 then goto countdown;
        ```
      ]
      #colbreak()
      ... we get the following output.
      #box(color: "#ffddff")[
        ```
        $ python interpreter.py countdown.blang
        5
        4
        3
        2
        1
        ```
      ]
    ]
  ]
]

= What now?

#pad(y: 10em)[
  #align(center)[
    = #link("https://github.com/rudsvar/booster-lang")
  ]
]
