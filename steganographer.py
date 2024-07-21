
import base64
import math

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from PIL import Image


# password = input("pw: ").encode()
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


def pixels_range(width, height, payload_len):
    """Generate the coordinates of chosen (payload-carrying) pixels in
    the carrier to be replaced by (or from which extract) the payload data.
    """

    # Intervals of chosen pixels (to load the payload in multiple rounds).
    rounds = 2
    # Reserve some pixels for steganography metadata.
    metadata_size = 4

    # Calculate density of payload within carrier's pixels.
    # Note: values are in number of pixels.
    carrier_capacity = width*height - metadata_size
    data_size = math.ceil(payload_len * 8 / 6)
    # Intervals of carrier pixels (to spread out the payload).
    # Reserve one pixel for the first data; and 'steps' equals to the number
    # of pixels that the rest of the data each occupy (including intervals).
    steps = math.floor((carrier_capacity-1) / (data_size-1))
    round_steps = steps * rounds

    for r in range(rounds):
        # Stating value of 'column' determines which round
        # of chosen pixels are getting filled.
        column = metadata_size + r*steps
        row = 0
        while row < height:  # Till the end of carrier file
            # If 'column' is out of bound, go to the next row
            # and continue from remainder of the interval.
            row += column // width
            column = column % width
            # Generate the position of the next chosen pixel.
            if row < height and column < width:
                yield row, column
            # Jump a whole step.
            column += round_steps


def stego_encrypt(carrier_file, payload_file, pw=None):
    """Hide every byte of a file (payload) inside another (carrier)."""

    img = Image.open(carrier_file)
    width, height = img.size
    pix = img.load()

    # Read binary data of the payload file.
    with open(payload_file, "rb") as bf:
        payload = bf.read()

    # Optionally, the payload can be encrypted before steganography.
    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        payload = cipher.encrypt(payload)

    pixels = pixels_range(width, height, len(payload))
    return list(pixels), len(payload)


# pixels, pl = stego_encrypt(carrier_file, file)
# pixels = pixels_range(4096, 2048, 455469)
pixels = pixels_range(14, 10, 21)




def stego_decrypt(stego_file, pw=None):
    """Extract the data hidden inside a file."""

    with open(stego_file, "rb") as bf:
        data = bf.read()

    # Do steganography here!

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(data)

    with open("result.mp3", "wb") as bf:
        bf.write(decrypted_data)
