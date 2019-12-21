# -*- coding: utf-8 -*-
from python_math_parser.tokenizer import Tokenizer
from python_math_parser.parser import Parser
from python_math_parser.interpreter import Interpreter

def tokenize():
    text = 'x = e - (3.14 + number) * matrix ** func(a, pi) # common math expression\n'
    print(text)
    token_iter = Tokenizer.token_iter(text)
    for token in token_iter:
        print(token)
    print('great, tokenize successfully!\n')

def parse():
    text = '''
        x = 1 + 2\n
        y = pi - log(3)\n
        z <= pi**2 - --e\n
        f(x, g(y)-10) >= (x-1)/(x**2+12)\n
        v = [3+pi, 5*x**2, e**(-(x-y))]\n
        m = [v, v, [e-pi, 1/pi, n/2]]\n
        s = {3, 9, m}\n
    '''
    print('--------------------------------------------------')
    print('Input text: ')
    print(text)
    token_iter = Tokenizer.token_iter(text)
    PSR = Parser(token_iter)
    ast = PSR.parse()
    print('--------------------------------------------------')
    print('Generated Ast: ')
    print(ast)
    cmd = Interpreter.interpret(ast)
    print('--------------------------------------------------')
    print('Interpreter cmd: ')
    print(cmd)

if __name__ == '__main__':
    tokenize()
    parse()


