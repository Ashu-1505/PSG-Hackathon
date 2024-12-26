from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf.csrf import CSRFProtect
from add import *
from send_otp import *
from encryption import *

def get_user_id_from_session():
    return session["user_id"]

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        hashes.SHA256(),
        length=32,  # Length of AES key (32 bytes for AES-256)
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for CSRF protection
csrf = CSRFProtect(app)

from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/get_otp', methods=['GET','POST'])
def get_otp():
    data = request.get_json()
    app.logger.info(f"Request received with data: {data}")
    connection = create_connection()
    username = data.get("username")
    password = data.get("password")
    
    if verify_user(username, password):
        send_otp(username)
        session['user_id'] = 1 
        session["key"] = password # Store user ID or other relevant data
        session['logged_in'] = True
        salt = os.urandom(16)  # Generate a random salt (stored securely)
        derived_key = derive_key(password, salt)
        
        # Store the derived key in the session (You can also store salt if needed)
        session['encryption_key'] = derived_key
        return jsonify({"success": True, "redirect_url": "/mfa"}), 200
    else:
        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

@app.route('/mfa')
def mfa():
    return render_template("mfa.html")

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    otp = data.get("otp")

    # Replace with actual OTP verification logic
    if otp == "123":  # Example OTP
        return jsonify({"success": True, "redirect_url": "/dashboard"})
    else:
        session.clear()
        return jsonify({"success": False, "message": "Invalid OTP", "redirect_url": "/login"}), 401

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dash.html')
    else:
        return redirect(url_for('login'))

@app.route('/passwords')
def passwords():
    if 'logged_in' in session and session['logged_in']:
        connection = create_connection()
        user_id = get_user_id_from_session()
        query = f"""SELECT * 
        FROM passwords 
        WHERE user_id = {session['user_id']}"""
        
        passwords = execute_query(connection, query)
        
        # Decrypt passwords before displaying them
        if passwords:
            for password in passwords:
                password['password'] = decrypt_password(password['encrypted_password'])
        else:
            passwords=[]
        
        return render_template('pass.html', passwords=passwords)
    else:
        return redirect(url_for('login'))

@app.route('/add_password', methods=['POST'])
def add_password():
    connection = create_connection()
    user_id = get_user_id_from_session()  # Get user id from the session
    password_name = request.form['password_name']
    password_value = request.form['password_value']
    expiration_value = request.form['expiration_value']
    password_category = request.form['password_category']
    
    # Encrypt the password before saving it to the database
    encrypted_password = encrypt_password(password_value)

    query = f"""
    INSERT INTO passwords (user_id, password_name, password_hash, expiration) 
    VALUES ({user_id}, '{password_name}', '{encrypted_password}', '{expiration_value}')
    """
    execute_query(connection, query)
    return redirect(url_for('passwords'))


@app.route('/folders')
def folders():
    if 'logged_in' in session and session['logged_in']:
        return render_template('folders.html')
    else:
        return redirect(url_for('login'))

@app.route('/audit')
def audit():
    if 'logged_in' in session and session['logged_in']:
        return render_template('audit.html')
    else:
        return redirect(url_for('login'))

@app.route('/breach')
def breach():
    if 'logged_in' in session and session['logged_in']:
        return render_template('breach.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
