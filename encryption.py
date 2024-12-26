from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from flask import session
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Function to pad the password (or data) to be encrypted for AES
def pad_data(data: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

# Encrypt password using AES and the key stored in the session
def encrypt_password(password: str) -> str:
    #key = session.get('encryption_key')
    key = os.urandom(32)
    if not key:
        raise Exception("Encryption key not found in session")
    
    salt = os.urandom(16)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padded_password = pad_data(password.encode())
    
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
    
    encrypted_data = base64.b64encode(salt + iv + encrypted_password).decode('utf-8')
    return encrypted_data

# Decrypt password using AES and the key stored in the session
def decrypt_password(encrypted_data: str) -> str:
    key = session.get('encryption_key')
    if not key:
        raise Exception("Encryption key not found in session")
    
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    
    salt = encrypted_data_bytes[:16]
    iv = encrypted_data_bytes[16:32]
    encrypted_password = encrypted_data_bytes[32:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(decrypted_padded_password) + unpadder.finalize()
    
    return password.decode('utf-8')
