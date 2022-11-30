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
#print(tree.toStringTree(recog=parser))
visitor = TreeVisitor()
visitor.visit(tree)
