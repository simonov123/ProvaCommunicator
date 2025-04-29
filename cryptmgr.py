#cryptmgr.py
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class cryptmgr:
    @staticmethod
    def keygen(msg):
        result = subprocess.run(
            ['./keygen.sh', msg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"{result.stderr}")
        return result.stdout.strip()

    def OTPcrypt(self, msg, key):
        result = subprocess.run(
            ['./en_dec.sh', msg, key],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"{result.stderr}")
        return result.stdout.strip()

    def encrypt_otp(self, otp_key):
        secret_key = get_random_bytes(16)
        cipher = AES.new(secret_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(otp_key.encode())
        encrypted_otp = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
        encrypted_secret_key = base64.b85encode(secret_key).decode()
        return encrypted_otp, encrypted_secret_key

    def decrypt_otp(self, encrypted_secret_key, encrypted_otp):
        # Decodifica le chiavi
        secret_key = base64.b85decode(encrypted_secret_key.encode())
        raw_data = base64.b64decode(encrypted_otp.encode())

        # Estrai nonce, tag e ciphertext
        nonce = raw_data[:16]
        tag = raw_data[16:32]
        ciphertext = raw_data[32:]

        # Decifra
        cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
        otp_key = cipher.decrypt_and_verify(ciphertext, tag)
        return otp_key.decode()
