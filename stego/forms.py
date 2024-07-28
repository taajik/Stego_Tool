
import uuid

from django import forms


class EncryptForm(forms.Form):
    carrier_file = forms.ImageField(
        label="The cover image",
        help_text="The Image to embed the data in.",
    )
    payload_file = forms.FileField(
        required=False,
        label="File",
        help_text="The file you want to hide.",
    )
    payload_text = forms.CharField(
        required=False,
        label="Text",
        widget=forms.Textarea,
        help_text="The text you want to hide.",
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Use password to encipher your data before steganography.",
    )

    def prepare_data(self):
        carrier = self.cleaned_data.get("carrier_file")
        payload_file = self.cleaned_data.get("payload_file")
        is_text = True
        payload_input = self.cleaned_data.get("payload_text")
        password = self.cleaned_data.get("password")

        carrier_name = f"media/{uuid.uuid4()}_{carrier.name}"
        with open(carrier_name, "wb+") as cf:
            for chunk in carrier.chunks():
                cf.write(chunk)

        if payload_file:
            is_text = False
            payload_input = f"media/{uuid.uuid4()}_{payload_file.name}"
            with open(payload_input, "wb+") as pf:
                for chunk in payload_file.chunks():
                    pf.write(chunk)

        if not password:
            password = None

        return carrier_name, payload_input, password, is_text


class DecryptForm(forms.Form):
    stego_file = forms.ImageField(
        label="The image",
        help_text="The Image containing the embedded data.",
    )
    is_text = forms.BooleanField(
        required=False,
        help_text="Is the embedded data just plain text?",
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        strip=False,
        help_text="Use password to decipher the data after steganography.",
    )

    def prepare_data(self):
        stego = self.cleaned_data.get("stego_file")
        is_text = self.cleaned_data.get("is_text")
        password = self.cleaned_data.get("password")

        stego_name = f"media/{uuid.uuid4()}_{stego.name}"
        with open(stego_name, "wb+") as cf:
            for chunk in stego.chunks():
                cf.write(chunk)

        if not password:
            password = None

        return stego_name, password, is_text
