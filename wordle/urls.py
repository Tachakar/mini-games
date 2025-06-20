from django.urls import path
from .views import WordleView
app_name = "wordle"

urlpatterns = [
    path("", WordleView.as_view(), name='index'),
]
