# -*- coding: utf-8 -*-
'''Parser for Math.

Referenced implementations:
    Parser for Pascal written in Python: 
        https://github.com/rspivak/lsbasi/blob/master/part17/spi.py
    Python's grammar: https://docs.python.org/3.6/reference/grammar.html

This implementaion of parser try to achieve: 
    the readability and simplicity of Pascal's.
    ablity to parse common math expressions, including vector, matrix, set, etc.

Math Grammar:
    - statement:
        compound_statement : statement*
        statement : equality |
                    empty 
        equality : expr (<=|>=|!=|=) expr
        empty : new_line+
    - expression grammar are ordered by priority level:
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

Parser.parse is the main program.
'''

from .tokenizer import Operator
from .ast import *

class Parser:
    def __init__(self, token_iter):
        '''Parser.
        Args:
            token_iter: token iterator returned by Tokenizer.
        '''
        self.token_iter = token_iter
        self.forward()
    def forward(self):
        '''Set current token by next(token_iter). '''
        self.current_token = next(self.token_iter)
    def error(self, error_code, token):
        '''Trigger by unexpected input. '''
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )
    def parse(self):
        """ generate ast. """
        node = self.compound_statement()

        if not self.current_token.is_eof():
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token,
            )
        return node
    ##########################################################
    # statement part
    ##########################################################
    def compound_statement(self):
        """
        compound_statement : statement*
        """
        node = self.statement()
        if self.current_token.is_eof():
            return node
        ops = [node]
        while not self.current_token.is_eof():
            ops.append(self.statement())
        node = CompoundOp(ops=ops)
        return node
    def statement(self):
        """
        statement : equality |
                    empty
        """
        if self.current_token.is_new_line():
            node = self.empty()
            return node
        node = self.equality()
        while self.current_token.is_new_line():
            self.forward()
        return node
    def equality(self):
        """ equality : expr = expr """
        left = self.expr()
        assert self.current_token.is_operator()
        relop = AtomOp(self.current_token, is_func=True)
        self.forward()
        right = self.expr()
        node = RelationOp(left, relop, right)
        return node
    def empty(self):
        """ empty : new_line+ """
        while self.current_token.is_new_line():
            self.forward()
        node = NoOp()
        return node

    ##########################################################
    # expression part 
    ##########################################################
    def expr(self):
        """ expr: set_expr|vec_expr|add_expr """
        if self.current_token.name == Operator.left_curly.name:
            node = self.set_expr()
        elif self.current_token.name == Operator.left_square.name:
            node = self.vec_expr()
        else:
            node = self.add_expr()
        return node
    def set_expr(self):
        """ set_expr: { arglist } """
        assert self.current_token.name == Operator.left_curly.name
        self.forward()
        ops = self.arglist()
        assert self.current_token.name == Operator.right_curly.name
        self.forward()
        node = SetOp(ops=ops)
        return node
    def vec_expr(self):
        """ vec_expr: [ arglist ] """
        assert self.current_token.name == Operator.left_square.name
        self.forward() 
        ops = self.arglist()
        assert self.current_token.name == Operator.right_square.name
        self.forward()
        node = VectorOp(ops=ops)
        return node
    def add_expr(self):
        """ add_expr: mul_expr ([+-] mul_expr)* """
        node = self.mul_expr()
        while self.current_token.name in (Operator.plus.name, 
                                          Operator.minus.name):
            op = AtomOp(self.current_token, is_func=True)
            self.forward()
            node = FuncOp(func=op, ops=[node, self.mul_expr()])
        return node
    def mul_expr(self):
        """ mul_expr: factor ([*/] factor)* """
        node = self.factor()
        while self.current_token.name in (Operator.multiply.name, 
                                          Operator.divide.name):
            op = AtomOp(self.current_token, is_func=True)
            self.forward()
            node = FuncOp(func=op, ops=[node, self.factor()])
        return node
    def factor(self):
        """ factor: [+-] factor | power """
        token = self.current_token
        if (token.name == Operator.minus.name 
            or token.name == Operator.plus.name):
            op = AtomOp(token, is_func=True)
            self.forward()
            node = FuncOp(func=op, ops=[self.factor()])
            return node
        else:
            node = self.power()
            return node
    def power(self):
        """ power: term [** factor] """
        node = self.term()
        if self.current_token.name == Operator.power.name:
            op = AtomOp(self.current_token, is_func=True)
            self.forward()
            node = FuncOp(func=op, ops=[node, self.factor()])
            return node
        return node
    def term(self):
        """ term: function | ( add_expr ) """
        if self.current_token.name == Operator.left_paren.name:
            self.forward()
            node = self.add_expr()
            assert self.current_token.name == Operator.right_paren.name
            self.forward()
        else:
            node = self.function() 
        return node
    def function(self):
        """ function: atom ( arglist? ) """
        assert (self.current_token.is_identifier() 
                or self.current_token.is_number())
        token = self.current_token
        self.forward()
        is_func = (self.current_token.name == Operator.left_paren.name)
        node = AtomOp(token, is_func=is_func)
        if self.current_token.name == Operator.left_paren.name:
            self.forward()
            arglist = []
            if self.current_token.name != Operator.right_paren.name:
                arglist = self.arglist()
            assert self.current_token.name == Operator.right_paren.name
            self.forward()
            node = FuncOp(func=node, ops=arglist)
        return node
    def arglist(self):
        """ arglist: expr (, expr)* """
        res = [self.expr()]
        while self.current_token.name == Operator.comma.name:
            self.forward()
            res.append(self.expr())
        return res




