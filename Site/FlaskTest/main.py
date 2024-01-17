from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name=name)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Что то постим'
    else:
        return 'Ничего не постим '




@app.route('/about/')
def about():
    return f'Page About!'

if __name__ == '__main__':

    app.run(debug = True)