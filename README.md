# stego tool

**A pure HTML/CSS interface for an image steganographer tool served with Django.**

Steganography, embeds data in a medium. In this app, the file used to embed data in (the carrier) is an image and the data (payload) can be any file format or just plain text.

> Image steganography is the practice of concealing information within the data of digital images without altering their visual appearance.[1]

This tool, implements the LSB (least significant bit) steganography method. Utilizing the minor effects of these bits on appearances of an image, the payload can be split into units of two bits and replace two least significant bits of a one-bit subpixel (each of the RGB values).

The core steganography functions written in Python can be found in [stego/steganographer.py](stego/steganographer.py) and used separately.


[1] [Image steganography: Concealing secrets within pixels](https://cybersecurity.att.com/blogs/security-essentials/image-steganography-concealing-secrets-within-pixels)
