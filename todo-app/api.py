from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

from backend import Todo

app = Flask(__name__)

@app.route("/api", methods=["GET", "POST"])
def set_todo():
    global todo
    todo = Todo("todo_data.json")
    return todo.data.model_dump()

app.run(debug=True)