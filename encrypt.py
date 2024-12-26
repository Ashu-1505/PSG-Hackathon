from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# Generate a 256-bit key using a password
password = b"your_password"  # Replace with a secure password
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# Encrypt the file
with open("Harshad_21PC15.pdf", "rb") as file:
    data = file.read()
iv = os.urandom(16)  # Initialization Vector
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(data) + encryptor.finalize()

# Save the encrypted file and salt/IV for decryption
with open("encrypted_file.pdf.enc", "wb") as encrypted_file:
    encrypted_file.write(salt + iv + encrypted_data)
