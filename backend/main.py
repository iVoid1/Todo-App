from flask import Flask
from flask_cors import CORS
from pathlib import Path

from app import TodoApp


app = Flask(__name__)
CORS(app)



