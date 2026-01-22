#set page(width: 20cm, height: 11cm)

#let slide(title, body) = [
  #block(breakable: false)[
    = #title
    #pad(top: 1em, body)
  ]
  #pagebreak()
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

#slide("Parsing a Program")[

  Parsing is all about making data more structured.
  We need to convert code to a model we can program with.

  #box[
    ```python
    @dataclass
    class Program:
      ...

    def parse_program(input: str) -> Program:
      ...
    ```
  ]
]

#slide("Parsing Expressions")[]
#slide("Parsing Statements")[]

#slide("Integers and Printing")[]
#slide("Variables")[]
#slide("If-statements")[]
#slide("Assignment")[]
#slide("While-loops")[]
#slide("Function Definitions")[]
#slide("Function Calls")[]
