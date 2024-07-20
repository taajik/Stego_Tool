
import base64
import math

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from PIL import Image


password = input("pw: ").encode()
file = "../Camel_Fingertips2.mp3"
carrier_file = "LDR_3_VPM_VISTA_STILL_digital_art_FINAL.png"


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


def stego_encrypt(carrier_file, payload_file, pw=None):
    """"""

    img = Image.open(carrier_file)
    width, height = img.size
    pix = img.load()

    with open(payload_file, "rb") as bf:
        payload = bf.read()

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        payload = cipher.encrypt(payload)

    # Calculate density of payload within carrier's pixels.
    carrier_capacity = width*height - 4
    data_size = math.ceil(len(payload) * 8 / 6)
    pixel_steps = math.floor(carrier_capacity / data_size)
    print(carrier_capacity, data_size, pixel_steps)


stego_encrypt(carrier_file, file)





def stego_decrypt(stego_file, pw=None):
    """"""

    with open(stego_file, "rb") as bf:
        data = bf.read()

    # Do steganography here!

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(data)

    with open("result.mp3", "wb") as bf:
        bf.write(decrypted_data)
