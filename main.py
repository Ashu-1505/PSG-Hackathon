from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for CSRF protection
csrf = CSRFProtect(app)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def dashboard():
    return render_template('dash.html')

@app.route('/passwords')
def passwords():
    return render_template('passwords.html')

@app.route('/folders')
def folders():
    return render_template('folders.html')

@app.route('/audit')
def audit():
    return render_template('audit.html')

if __name__ == '__main__':
    app.run(debug=True)
