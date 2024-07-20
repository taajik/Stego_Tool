
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


password = input("pw: ").encode()


def gen_key(pw):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\x19\x04\x99\x88\xeeZ\xd9\xd1\x04n>M\xa4\x9a\xd6\x16',
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(pw)).decode()



key = gen_key(password)
data = "my secret".encode()
cipher = Fernet(key)

encrypted_data = cipher.encrypt(data)
print(encrypted_data.decode())


decrypted_data = cipher.decrypt(encrypted_data)
print(decrypted_data.decode())
