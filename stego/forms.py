
from django import forms

from .steganographer import stego_encrypt


class EncryptForm(forms.Form):
    payload = forms.FileField(help_text="The file you want to hide.")
    carrier = forms.ImageField(help_text="The Image to embed the data in.")

    def encrypt(self):
        print(self.cleaned_data["payload"])
        print(self.cleaned_data["carrier"])
