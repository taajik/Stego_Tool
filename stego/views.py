
from django.http import StreamingHttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import EncryptForm
from .steganographer import stego_encrypt


class EncryptFormView(FormView):
    template_name = "stego/encrypt.html"
    form_class = EncryptForm
    success_url = reverse_lazy("stego:result")

    def form_valid(self, form):
        carrier_name, payload, is_text = form.save_files()
        self.request.session["is_encrypt"] = True
        self.request.session["carrier"] = carrier_name
        self.request.session["payload"] = payload
        self.request.session["is_text"] = is_text
        return super().form_valid(form)


class ResultView(TemplateView):
    template_name = "stego/result.html"


def run_stego(is_encrypt, carrier_file, payload_input, is_text):
    if is_encrypt:
        stego_encrypt(carrier_file, payload_input, is_text=is_text)
    yield "/" + carrier_file


def process_result(request):
    response = StreamingHttpResponse(
        run_stego(
            request.session["is_encrypt"],
            request.session["carrier"],
            request.session["payload"],
            request.session["is_text"],
        ),
        status=200,
        content_type="text/event-stream"
    )
    return response
