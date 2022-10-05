from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return 'Login page'

@app.route('/signup')
def signup():
    return 'Signup page'

@app.route('/backlog')
def backlog():
    return 'Backlog page'

@app.route('/signout')
def signout():
    return 'signout page'