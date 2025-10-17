from django.urls import path
from .views import *
app_name = 'tictactoe'

urlpatterns = [
    path("", TictactoeStartScreen.as_view(), name="index")
]
