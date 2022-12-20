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
        try:
            self.tree_visitor.visit(tree)
            output = self.tree_visitor.getOutputBuffer()
            if len(output) == 0:
                output = ["None"]
            self.io_buffer.append((code, "\n".join(output)))
        except Exception as e:
            self.io_buffer.append((code, e))

    def getIObuffer(self):
        return self.io_buffer

    # statics are global context elements, aka functions and global variables
    def getStatics(self):
        return self.tree_visitor.getStatics()


app = Flask(__name__)
funx_executer = FunxExecuter()


@app.route('/', methods=['GET', 'POST'])
def base():
    # the user has introduced some code
    if request.method == 'POST':
        new_code = request.form["codearea"]
        funx_executer.execute(new_code)
        return render_template('base.html',
                               name="ok",
                               io_buffer=funx_executer.getIObuffer(),
                               statics=funx_executer.getStatics())
    # the user hasn't yet inserted any code
    else:
        return render_template('base.html', name="default")
