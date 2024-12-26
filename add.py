import bcrypt
import mysql.connector
from conn import *
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to add a user to the database
def add_user(username, email, plain_password):
    connection = create_connection()
    hashed_password = hash_password(plain_password).decode('utf-8')  # Decode to store as string
    query = f"""
    INSERT INTO users (username, email, password_hash) 
    VALUES ('{username}', '{email}', '{hashed_password}')
    """
    execute_query(connection, query)


def verify_user(username, plain_password):
    connection = create_connection()
    query = f"SELECT password_hash FROM users WHERE username = '{username}'"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        stored_hash = result[0]  # Get the stored hash from the query result
        if bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8")):
            print("Password is correct.")
            return True
        else:
            print("Password is incorrect.")
            return False
    else:
        print("Username not found.")
        return False

#add_user("user1","ashurhsa@gmail.com","User@123")
#verify_user("user1", "User@123")