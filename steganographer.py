
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


password = input("pw: ").encode()
file = "/home/aaronn/Documents/TEMP/Camel_Fingertips2.mp3"


def gen_key(pw):
    """Generate a symmetric key based on a password."""

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\x19\x04\x99\x88\xeeZ\xd9\xd1\x04n>M\xa4\x9a\xd6\x16',
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(pw)).decode()


def stego_encrypt(file, pw=None):
    """"""

    with open(file, "rb") as bf:
        data = bf.read()

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(data)

    print(type(data))
    print(data[:100])
    print(list(data[:100]))
    print(type(encrypted_data))
    print(encrypted_data[:100])


# stego_encrypt(file)
stego_encrypt(file, password)





def stego_decrypt(file, pw=None):
    """"""

    with open(file, "rb") as bf:
        data = bf.read()

    # Do steganography here!

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(data)

    with open("result.mp3", "wb") as bf:
        bf.write(decrypted_data)
