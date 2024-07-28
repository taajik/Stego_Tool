
import json

from django.http import StreamingHttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import EncryptForm, DecryptForm
from .steganographer import stego_encrypt, stego_decrypt


class EncryptFormView(FormView):
    template_name = "stego/encrypt.html"
    form_class = EncryptForm
    success_url = reverse_lazy("stego:result")

    def form_valid(self, form):
        carrier_file, payload_input, password, is_text = form.prepare_data()
        self.request.session["is_encrypt"] = True
        self.request.session["image"] = carrier_file
        self.request.session["payload_input"] = payload_input
        self.request.session["password"] = password
        self.request.session["is_text"] = is_text
        return super().form_valid(form)


class DecryptFormView(FormView):
    template_name = "stego/decrypt.html"
    form_class = DecryptForm
    success_url = reverse_lazy("stego:result")

    def form_valid(self, form):
        stego_file, password, is_text = form.prepare_data()
        self.request.session["is_encrypt"] = False
        self.request.session["image"] = stego_file
        self.request.session["password"] = password
        self.request.session["is_text"] = is_text
        return super().form_valid(form)


class ResultView(TemplateView):
    template_name = "stego/result.html"


def run_stego(is_encrypt, image, payload_input, password, is_text):
    if is_encrypt:
        result = stego_encrypt(image, payload_input, password, is_text)
    else:
        result = stego_decrypt(image, password, is_text)

    is_text = (not is_encrypt) and is_text
    yield json.dumps({"result":[result, is_text]})


def process_result(request):
    response = StreamingHttpResponse(
        run_stego(
            is_encrypt=request.session.get("is_encrypt"),
            image=request.session.get("image"),
            payload_input=request.session.get("payload_input"),
            password=request.session.get("password"),
            is_text=request.session.get("is_text"),
        ),
        status=200,
        content_type="application/json",
    )
    return response
