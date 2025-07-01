from django.urls import path
from .views import WordleView, StartScreen
app_name = "wordle"

urlpatterns = [
    path("", StartScreen.as_view(), name='index'),
    path("<int:pk>/", WordleView.as_view(), name='game')
]
