from django.urls import path
from . import views
app_name = "wordle"

urlpatterns = [
    path("", views.main, name='main'),
]
