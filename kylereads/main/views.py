from flask import render_template
from . import main

@main.route('/')
def root():
    return render_template('index.html')
