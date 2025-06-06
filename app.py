from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/about')
def about():
    num = 42
    return f'This is the About page Number:{num}'

@app.route('/contact')
def contact():
    return ""

if __name__ == "__main__":

    app.run(debug=True)