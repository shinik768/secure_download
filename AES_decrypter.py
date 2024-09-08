from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import io
import os

# AES復号化関数
def decrypt_pdf(input_file, private_key):
    # 暗号化されたPDFファイルを読み込み
    with open(input_file, 'rb') as f:
        nonce = f.read(16)      # 最初の16バイトはnonce（初期化ベクトル）
        tag = f.read(16)        # 次の16バイトは認証タグ
        encrypted_key = f.read(256)  # 次の256バイトは暗号化されたAES鍵
        ciphertext = f.read()   # 残りは暗号化されたデータ

    # 秘密鍵を用いてAES鍵を復号化
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    key = rsa_cipher.decrypt(encrypted_key)

    # 復号化を実行
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_pdf = cipher.decrypt_and_verify(ciphertext, tag)
    
    decrypted_pdf_stream = io.BytesIO(decrypted_pdf)
    return decrypted_pdf_stream

def execute_decrypt():
    # 復号化するPDFファイルのパス
    encrypted_pdf = f"{os.getenv('PDF_DIRECTORY', '7NduUHW9hrTM9smgrrNVNv53ZEMTpMZcJGEWt9ur')}/encrypted.pdf"  # 復号化するPDFファイル

    with open('/etc/secrets/private.pem', 'rb') as f:
        private_key = f.read()

    # 復号化の実行
    decrypt_pdf_stream = decrypt_pdf(encrypted_pdf, private_key) 

    print("PDFファイルが復号化されました。")

    return decrypt_pdf_stream
