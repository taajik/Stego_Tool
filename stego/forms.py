
import uuid

from django import forms


class EncryptForm(forms.Form):
    carrier = forms.ImageField(help_text="The Image to embed the data in.")
    payload_file = forms.FileField(
        required=False,
        help_text="The file you want to hide."
    )
    payload_text = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text="The text you want to hide."
    )

    def save_files(self):
        carrier = self.cleaned_data.get("carrier")
        payload_file = self.cleaned_data.get("payload_file")
        is_text = True
        payload_input = self.cleaned_data.get("payload_text")

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

        return carrier_name, payload_input, is_text
