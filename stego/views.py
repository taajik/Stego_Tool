
from django.views.generic.edit import FormView

from .forms import EncryptForm


class EncryptFormView(FormView):
    template_name = "stego/encrypt.html"
    form_class = EncryptForm
    success_url = "/result/"

    def form_valid(self, form):
        form.encrypt()
        return super().form_valid(form)
