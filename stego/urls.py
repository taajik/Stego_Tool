
from django.urls import path

from . import views


app_name = "stego"

urlpatterns = [
    path("", views.EncryptFormView.as_view(), name="encrypt"),
    path("result/", views.ResultView.as_view(), name="result"),
    path("process/", views.process_result, name="process"),
]
