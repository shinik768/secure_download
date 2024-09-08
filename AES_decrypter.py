from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import io
import os

def decrypt_pdf(input_file, private_key):
    with open(input_file, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        encrypted_key = f.read(256)
        ciphertext = f.read()

    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    key = rsa_cipher.decrypt(encrypted_key)

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_pdf = cipher.decrypt_and_verify(ciphertext, tag)
    
    decrypted_pdf_stream = io.BytesIO(decrypted_pdf)
    return decrypted_pdf_stream

def execute_decrypt():
    encrypted_pdf = f"{os.getenv('PDF_DIRECTORY')}/encrypted.pdf"

    with open('/etc/secrets/private.pem', 'rb') as f:
        private_key = f.read()

    decrypt_pdf_stream = decrypt_pdf(encrypted_pdf, private_key) 

    return decrypt_pdf_stream
