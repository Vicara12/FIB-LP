#!/bin/python3

from antlr4 import *
from FunxLexer import FunxLexer
from FunxParser import FunxParser
from TreeVisitor import TreeVisitor
import sys

input_stream = FileStream(sys.argv[1])

lexer = FunxLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = FunxParser(token_stream)
tree = parser.root()

visitor = TreeVisitor()
try:
    visitor.visit(tree)
except Exception as e:
    print(e)
