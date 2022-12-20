#!/bin/python3

from flask import Flask, render_template, request
from antlr4 import *
from FunxLexer import FunxLexer
from FunxParser import FunxParser
from TreeVisitor import TreeVisitor
# from io import StringIO


class FunxExecuter:
    def __init__(self):
        self.functions = {}
        self.tree_visitor = TreeVisitor()
        self.tree_visitor.setOutputToBuffer(True)
        self.io_buffer = []

    def execute(self, code):
        file = open("new_code.funx", "w")
        file.write(code)
        file.close()
        # code_stream = StringIO(code)
        code_stream = FileStream("new_code.funx")
        lexer = FunxLexer(code_stream)
        token_stream = CommonTokenStream(lexer)
        parser = FunxParser(token_stream)
        tree = parser.root()
        self.tree_visitor.visit(tree)
        self.io_buffer.append((code,
                               "\n".join(self.tree_visitor.getOutputBuffer())))
        print(self.io_buffer[-1])


app = Flask(__name__)
funx_executer = FunxExecuter()


@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        new_code = request.form["codearea"]
        funx_executer.execute(new_code)
        return render_template('base.html', name="ok")
    else:
        return render_template('base.html', name="default")
