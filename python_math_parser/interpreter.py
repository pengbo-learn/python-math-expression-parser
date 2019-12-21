# -*- coding: utf-8 -*-
''' Simple interpreter for visiting ast.

Referenced implementations:
    Interpreter for Pascal written in Python: 
        https://github.com/rspivak/lsbasi/blob/master/part17/spi.py

Interpreter.interpret is the main program.
'''
from .tokenizer import Operator

class Interpreter:
    def __init__(self, root):
        pass
    @classmethod
    def visit(cls, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(cls, method_name, cls.visit_generic)
        return visitor(node)
    @classmethod
    def visit_generic(cls, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    ##########################################################
    # expression part 
    ##########################################################
    @classmethod
    def visit_AtomOp(cls, node):
        if node.is_func:
            res = 'Func("{}")'.format(node)
        else:
            res = 'atom("{}")'.format(node)
        return res
    @classmethod
    def visit_FuncOp(cls, node):
        func = cls.visit(node.func)
        symbols = [cls.visit(x) for x in node.ops]
        args = ', '.join([str(x) for x in symbols])
        res = '{}.eval({})'.format(func, args)
        return res
    @classmethod
    def visit_VectorOp(cls, node):
        symbols = [cls.visit(x) for x in node.ops]
        args = ', '.join([str(x) for x in symbols])
        res = 'vector({})'.format(args)
        return res
    @classmethod
    def visit_SetOp(cls, node):
        symbols = [cls.visit(x) for x in node.ops]
        args = ', '.join([str(x) for x in symbols])
        res = 'set({})'.format(args)
        return res
    ##########################################################
    # statement part
    ##########################################################
    @classmethod
    def visit_CompoundOp(cls, node):
        cmds = [cls.visit(op) for op in node.ops]
        res = '\n'.join(cmds)
        return res
    @classmethod
    def visit_RelationOp(cls, node):
        symbol = cls.visit(node.symbol)
        r_symbol = cls.visit(node.r_symbol)
        op = cls.visit(node.op)
        res = '{}({}, {})'.format(op, symbol, r_symbol)
        return res
    @classmethod
    def visit_NoOp(cls, node):
        return ''
    @classmethod
    def interpret(cls, root):
        if root is None:
            return ''
        return cls.visit(root)

