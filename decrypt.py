from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

password = b"your_password"
# Read the encrypted file
with open("encrypted_file.pdf.enc", "rb") as encrypted_file:
    encrypted_content = encrypted_file.read()

salt = encrypted_content[:16]
iv = encrypted_content[16:32]
encrypted_data = encrypted_content[32:]

# Re-generate the key using the same password and salt
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# Decrypt the data
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

# Save the decrypted PDF
with open("decrypted_file.pdf", "wb") as file:
    file.write(decrypted_data)
