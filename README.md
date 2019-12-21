# Python Math Parser

A simple math expression parser written in python.

## Features

- Support basic operations: Plus(+), Minus(-), Multiply(\*), Divide(/), Power(\*\*)

- Support parenthesis nesting: (1 * (2 / (3 - 2)))

- Support unary operation: Plus(+), Minus(-)

- Support multi-variable function nesting: f(1, b, g(h, pi))

- Support Vector expression: [a\*\*b, 2/pi, f(3, pi)]

- Support Set expression: {a, f(pi), e}

## Implementation

- The parser is LL(1).
- The code is mainly based on [Let's Build A Simple Interpreter](https://github.com/rspivak/lsbasi/blob/master/part17/spi.py).
- To make it more compact, tokenization is based on python's re module, like [Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html).
- The grammar is mainly based on [Python's grammar](https://docs.python.org/3/reference/grammar.html).
- Most effort is spent on making code simple.

## Tokenization
```txt
    -------------------------------------------------------------
    | tokens       | regex                                      |
    |-----------------------------------------------------------|
    | comment      | #[^\n\r]*                                  |
    | space        | [ \t]+                                     |
    | number       | digits (. digits)?                         |
    | identifier   | letter_(letter_|digit)*                    |
    | operator     | >= | <= | ** | [-+*/()<>[\]{}]             |
    | new_line     | [\n\r]                                     |
    -------------------------------------------------------------
```

## Grammar

- statement:
    ```txt
    compound_statement : statement*
    statement : equality |
                empty 
    equality : expr (<=|>=|!=|=) expr
    empty : new_line+
    ```
- expression grammar are ordered by priority level:
    ```txt
    expr: set_expr|vec_expr|add_expr
    set_expr: { arglist }
    vec_expr: [ arglist ]
    add_expr: mul_expr ([+-] mul_expr)*
    mul_expr: factor ([*/] factor)*
    factor: [+-] factor | power
    power: term [** factor] | factor
    term: function | ( add_expr ) 
    function: atom ( arglist? )    
    arglist: expr (, expr)*    
    ```

## Run
```python
$ python run.py 
x = e - (3.14 + number) * matrix ** func(a, pi) # common math expression

Token(identifier, 'x')
Token(equal, '=')
Token(identifier, 'e')
Token(minus, '-')
Token(left_paren, '(')
Token(number, '3.14')
Token(plus, '+')
Token(identifier, 'number')
Token(right_paren, ')')
Token(multiply, '*')
Token(identifier, 'matrix')
Token(power, '**')
Token(identifier, 'func')
Token(left_paren, '(')
Token(identifier, 'a')
Token(comma, ',')
Token(identifier, 'pi')
Token(right_paren, ')')
Token(new_line, '\n')
Token(eof, '')
great, tokenize successfully!

--------------------------------------------------
Input text: 

        x = 1 + 2

        y = pi - log(3)

        z <= pi**2 - --e

        f(x, g(y)-10) >= (x-1)/(x**2+12)

        v = [3+pi, 5*x**2, e**(-(x-y))]

        m = [v, v, [e-pi, 1/pi, n/2]]

        s = {3, 9, m}

    
--------------------------------------------------
Generated Ast: 

x = plus(1, 2)
y = minus(pi, log(3))
z <= minus(power(pi, 2), minus(minus(e)))
f(x, minus(g(y), 10)) >= divide(minus(x, 1), plus(power(x, 2), 12))
v = [plus(3, pi), multiply(5, power(x, 2)), power(e, minus(minus(x, y)))]
m = [v, v, [minus(e, pi), divide(1, pi), divide(n, 2)]]
s = {3, 9, m}
--------------------------------------------------
Interpreter cmd: 

Func("equal")(atom("x"), Func("plus").eval(atom("1"), atom("2")))
Func("equal")(atom("y"), Func("minus").eval(atom("pi"), Func("log").eval(atom("3"))))
Func("less_equal")(atom("z"), Func("minus").eval(Func("power").eval(atom("pi"), atom("2")), Func("minus").eval(Func("minus").eval(atom("e")))))
Func("greater_equal")(Func("f").eval(atom("x"), Func("minus").eval(Func("g").eval(atom("y")), atom("10"))), Func("divide").eval(Func("minus").eval(atom("x"), atom("1")), Func("plus").eval(Func("power").eval(atom("x"), atom("2")), atom("12"))))
Func("equal")(atom("v"), vector(Func("plus").eval(atom("3"), atom("pi")), Func("multiply").eval(atom("5"), Func("power").eval(atom("x"), atom("2"))), Func("power").eval(atom("e"), Func("minus").eval(Func("minus").eval(atom("x"), atom("y"))))))
Func("equal")(atom("m"), vector(atom("v"), atom("v"), vector(Func("minus").eval(atom("e"), atom("pi")), Func("divide").eval(atom("1"), atom("pi")), Func("divide").eval(atom("n"), atom("2")))))
Func("equal")(atom("s"), set(atom("3"), atom("9"), atom("m")))
```

## References
- [Let's Build A Simple Interpreter](https://github.com/rspivak/lsbasi/blob/master/part17/spi.py)\
- [Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html)\
- [Python's grammar](https://docs.python.org/3/reference/grammar.html)

