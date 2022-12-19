#!/bin/python3

from flask import Flask, render_template, request
app = Flask(__name__)
from random import random

@app.route('/', methods = ['GET','POST'])
def base():
    if request.method == 'POST':
        print(request.form)
        return render_template('base.html', name = "ok")
    else:
        return render_template('base.html', name = "default")
