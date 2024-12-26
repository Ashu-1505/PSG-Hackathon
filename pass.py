
def get_passwords():
    user_password = request.form['user_password']  # User's password to generate key for AES decryption
    user_id = get_user_id_from_session()
    query = f"SELECT * FROM passwords WHERE user_id = {user_id}"
    passwords = execute_query(connection, query)

    # Decrypt the password before displaying
    for password in passwords:
        password['password'] = decrypt_password(password['password_hash'], user_password)
    
    return render_template('passwords.html', passwords=passwords)