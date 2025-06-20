from django.urls import path
from .views import Index
app_name = "tictactoe"
urlpatterns = [
    path("", Index.as_view(), name='index')
]
