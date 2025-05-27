from django.urls import path
from django.views.generic import TemplateView
from .views import Main
app_name = "wordle"

urlpatterns = [
    path("", Main.as_view(), name='main'),
]
