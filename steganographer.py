
import base64
import math

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from PIL import Image


# password = input("pw: ").encode()
file = "../Frank Sinatra_The World We Knew (Over And Over).mp3"
carrier_file = "LDR_3_VPM_VISTA_STILL_digital_art_FINAL.png"

# Reserve some pixels for steganography metadata.
METADATA_SIZE = 4
# metadata size in bytes = (METADATA_SIZE pixels * 3 subpixels * 2 LSBs) / 8
METADATA_BYTES = METADATA_SIZE * 3 // 4


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

    # Calculate density of payload within carrier's pixels.
    # Note: values are in number of pixels.
    carrier_capacity = width*height - METADATA_SIZE
    # Number of pixels requiered to store all of the payload data:
    # Three units of data can be stord in a pixel (one in each subpixel (RGB)).
    # Each unit of data is two bits.
    data_size = math.ceil(payload_len * 8 / 6)
    if data_size > carrier_capacity:
        raise OverflowError("payload can't fit in this carrier file")

    # Generate positions of the metadata.
    for j in range(METADATA_SIZE):
        i = j // width
        for c in range(3):
            if j == METADATA_SIZE-1 and c == j%4:
                # Remainder of the metadata in the last pixel doesn't
                # necessarily take all three subpixels.
                break
            yield i, j%width, c

    # Intervals of carrier pixels (to spread out the payload):
    # Reserve one pixel for the first unit of data; and for the rest:
    # 'steps' equals to the number of pixels that each
    # unit of data occupies (one payload-carrying plus intervals).
    steps = math.floor((carrier_capacity-1) / (data_size-1))
    # Intervals of chosen pixels (to load the payload in multiple rounds):
    ROUNDS = 2
    round_steps = steps * ROUNDS

    for r in range(ROUNDS):
        # Stating value of 'column' determines which round
        # of chosen pixels are getting filled.
        column = METADATA_SIZE + r*steps
        row = 0
        while row < height:  # Till the end of carrier file
            # If 'column' is out of bound, go to the next row
            # and continue from remainder of the interval.
            row += column // width
            column = column % width
            # Generate positions of the chosen pixels.
            if row < height and column < width:
                # c corresponds to the RGB subpixels.
                # So the same pixel coordinate is returned three times.
                for c in range(3):
                    yield row, column, c
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

    payload_len = len(payload)
    # Biggest 'payload_len' that can be stored in 'METADATA_SIZE' pixels:
    if payload_len > 2**(METADATA_BYTES*8) - 1:
        raise ValueError("payload is too large")
    payload = int.to_bytes(payload_len, METADATA_BYTES, "big") + payload

    # Designated positions for the rest of data in carrier's pixels:
    positions = iter(pixels_range(width, height, payload_len))

    # Load the data into the carrier.
    # Every byte of data is split into four sections of two bits and
    # each one of these units are stored in two LSBs of a subpixel.
    for data_byte in payload:
        for quarter in range(0, 8, 2):
            i, j, c = next(positions)
            # Remove the two least significant bits of the subpixel
            # and replace them with the next unit of data.
            new_px = list(pix[j, i])
            # NEEDS A COMMENT:
            new_px[c] = (pix[j, i][c] & 252) | (data_byte>>quarter & 3)
            pix[j, i] = tuple(new_px)

    img.save(carrier_file)


stego_encrypt(carrier_file, file)
# pixels = pixels_range(4096, 2048, 455469)
# pixels = pixels_range(14, 10, 21)
# pixels = pixels_range(14, 10, 90)

# max_payload_bytes = math.floor((width*height - METADATA_SIZE) * 0.75)




def stego_decrypt(stego_file, pw=None):
    """Extract the data hidden inside a file."""

    img = Image.open(stego_file)
    width, height = img.size
    pix = img.load()

    # Do steganography here!
    # payload_len = int.from_bytes(pix[:METADATA_SIZE], "big")
    # payload = pix[METADATA_SIZE:payload_len]

    if pw is not None:
        key = gen_key(pw)
        cipher = Fernet(key)
        payload = cipher.decrypt(payload)

    with open("embedded_payload", "wb") as bf:
        bf.write(payload)
