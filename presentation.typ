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
  #pad(y: 2em)[
    #box[
      ```rust
      $ let hello = "Hello Booster!";
      $ let booster = "Booster!"
      $ print(+ hello booster)
      Hello Booster!
      ```
    ]
  ]
  #text(fill: rgb("#555555"))[
      *Preparation*

      1. Install Python: https://www.python.org/downloads/
      2. Install Visual Studio Code: https://code.visualstudio.com/
      3. Install the Python plugin
      4. Clone https://github.com/rudsvar/booster-lang
    ]
]

#slide("How do we start?")[
  We need to make a program that runs another program.
  #pad(y: 4em)[
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
]

#slide("Interpreting in three steps")[
  #grid(columns: (1fr, 1fr), row-gutter: 3em,
    align(horizon)[Define types that represent the program,],
    box[
      ```python
      type Statement = Print | Let | ...
      type Program = list[Statement]
      ```
    ],
    align(horizon)[then *parse* the code into the types we defined,],
    box[
      ```python
      def parse_program(code: str) -> Program:
        for line in code.split(';'):
          # ...
      ```
    ],
    align(horizon)[and finally *execute* the program.],
    box[
      ```python
      def execute_program(program: Program):
        for statement in program:
          # ...
      ```
    ],
  )
]

#slide("What will our language look like?")[

  We keep the syntax and functionality a bit limited to make it simple enough for a workshop.

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
