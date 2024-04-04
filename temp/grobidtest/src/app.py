from grobid import parse_pdf
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<p>Hello World!</p>'

def main():
    parse_pdf()
    return 

# if __name__ == "__main__":
    # main()