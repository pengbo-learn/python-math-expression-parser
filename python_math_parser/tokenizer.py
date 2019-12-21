# -*- coding: utf-8 -*-
'''Tokenizer implementation. 

Referenced implementations:
    Tokenizer for Pascal written in Python: 
        https://github.com/rspivak/lsbasi/blob/master/part17/spi.py
    Python's official tokenizer: 
        https://github.com/python/cpython/blob/3.8/Lib/tokenize.py

This implementaion of tokenizer try to achieve: 
    the readability and simplicity of Pascal's tokenizer
    utilizing regular expression like python's official tokenizer.

Preknowledge:
    1.Lexemes are matched by patterns to form tokens.
        ---------------------------------------------------------
        | convetions        | definitions                       |
        |-------------------------------------------------------|
        | digit             | [0-9]                             |
        | digits            | digit+                            |
        |-------------------------------------------------------| 
        | letter            | [a-zA-Z]                          |
        | letter_           | (letter | _)                      |
        ---------------------------------------------------------

        -------------------------------------------------------------
        | tokens       | regex                                      |
        |-----------------------------------------------------------|
        | comment      | #[^\n\r]*                                  |
        | space        | [ \t]+                                     |
        | number       | digits (. digits)?                         |
        | identifier   | letter_(letter_|digit)*                    |
        | operator     | [><!]= | ** | [-+*/=<>()[\]{},]            |
        | new_line     | [\n\r]                                     |
        -------------------------------------------------------------

    Tables are mainly collected from "chaper3 lexical analysis" of Compilers: Principles, Techniques, and Tools.

    2.Each lexeme pattern could be represented by a regex, the latter could be solved by a NFA or DFA.
    We directly use python's re module for matching regular expression, for brevity.

Tokenizer.token_iter is the main program.
'''


import re
import pdb
from enum import Enum

class Token:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        res = 'Token({}, {})'.format(
            self.name, repr(self.value))
        return res
    def __repr__(self):
        return self.__str__()
    def is_identifier(self):
        return self.name == Tokenizer.identifier.name
    def is_number(self):
        return self.name == Tokenizer.number.name
    def is_operator(self):
        return hasattr(Operator, self.name) 
    def is_new_line(self):
        return self.name == Tokenizer.new_line.name
    def is_eof(self):
        return self.name == Tokenizer.eof.name

class Operator(Enum):
    # 2 characters
    power = '**'
    less_equal = '<='
    greater_equal = '>='
    not_equal = '!='
    # 1 character
    plus = '+'
    minus = '-'
    multiply = '*'
    divide = '/'
    equal = '='
    less_than = '<'
    greater_than = '>'
    left_curly = '{'
    left_paren = '('
    left_square = '['
    right_curly = '}'
    right_paren = ')'
    right_square = ']'
    comma = ','

class Tokenizer(Enum):
    comment = r'#[^\r\n]*'
    space = r'[ \t]+'
    identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'
    number = r'[0-9]+(?:\.[0-9]*)?'
    operator = r'\*\*|[<>!]=|[-+*/=<>()[\]{},]'
    new_line = r'[\r\n]'
    eof = r'$'
    error = r'(.+?)'
    @classmethod
    def _build_pattern(cls):
        cls.names = [x.name for x in cls]
        cls.regex = '|'.join('({})'.format(x.value) for x in cls)
        cls.pattern = re.compile(cls.regex)
    @classmethod
    def token_iter(cls, text):
        ''' text to token iter. 
        Args:
            text: string for tokenization.
        Returns:
            Iteration object of generated tokens.
        '''
        for match in cls.pattern.finditer(text):
            name = cls.names[match.lastindex-1]
            # skip space and comment
            if (name == cls.space.name 
                or name == cls.comment.name):
                continue
            # raise error
            elif name == cls.error.name:
                print(text[match.start():])
                import pdb
                pdb.set_trace()
                raise Exception('Invalid Syntax.')
            value = match.group()
            # operator name
            if name == cls.operator.name:
                name = Operator(value).name
            token = Token(name, value)
            yield token
Tokenizer._build_pattern()




