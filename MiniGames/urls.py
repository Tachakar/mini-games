from django.contrib import admin
from django.urls import include, path
app_name = 'base'
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls"), name="home"),
    path("wordle/", include("wordle.urls"), name='wordle'),
    path("tictactoe/", include("tictactoe.urls"), name='tictactoe'),
]
