import os

from flask import Flask, redirect, request, send_file, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/README.md')

@app.route('/README.md')
def send_static_file():
    filename = os.path.join(app.root_path, request.path[1:])
    with open(filename, 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
