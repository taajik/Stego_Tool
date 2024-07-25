
from django.urls import path

from . import views


urlpatterns = [
    path("", views.EncryptFormView.as_view(), name="encrypt")
]
