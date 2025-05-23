from django.urls import path
from . import views
app_name = "home"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("login/", views.login, name="login"),
]
