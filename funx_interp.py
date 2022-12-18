#!/bin/python3

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def base():
    name = "Victor"
    return render_template('base.html', name = name)
