# -*- coding: utf-8 -*-
''' Ast for math.

Referenced implementations:
    Ast for Pascal written in Python: 
        https://github.com/rspivak/lsbasi/blob/master/part17/spi.py

This implementaion of ast try to achieve: 
    - simplicity.
    - generality. 

expression nodes:
    AtomOp, FuncOp, VectorOp, SetOp
statement nodes:
    CompoundOp, RelationOp, NoOp
'''

class AST:
    def __init__(self, token):
        self.token = token
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return str(self.token)

##########################################################
# expression part 
##########################################################
class AtomOp(AST):
    def __init__(self, token, is_func=False):
        self.token = token
        self.value = token.value
        self.is_func = is_func
    def __str__(self):
        if self.token.is_operator():
            return self.token.name
        return self.value
class FuncOp(AST):
    def __init__(self, func=None, ops=None):
        self.func = func
        self.ops = ops
    def __str__(self):
        pstr = ', '.join([str(x) for x in self.ops])
        return '{}({})'.format(self.func, pstr)
class VectorOp(AST):
    def __init__(self, ops=None):
        self.ops = ops
    def __str__(self):
        pstr = ', '.join([str(x) for x in self.ops])
        return '[{}]'.format(pstr)
class SetOp(AST):
    def __init__(self, ops=None):
        self.ops = ops
    def __str__(self):
        pstr = ', '.join([str(x) for x in self.ops])
        return '{'+pstr+'}'


##########################################################
# statement part
##########################################################
class CompoundOp(AST):
    def __init__(self, ops=None):
        self.ops = ops
    def __str__(self):
        res = '\n'.join([str(x) for x in self.ops])
        return res


class RelationOp(AST):
    def __init__(self, symbol, op, r_symbol):
        self.symbol = symbol
        self.op = op
        self.r_symbol = r_symbol
    def __str__(self):
        res = '{} {} {}'.format(self.symbol, self.op.value, self.r_symbol)
        return res


class NoOp(AST):
    def __init__(self):
        pass
    def __str__(self):
        return ''







