from django.urls import path
from .views import WordleView, StartScreen, NewGame, CheckGameState, GameHistoryView
app_name = "wordle"

urlpatterns = [
    path("", StartScreen.as_view(), name='index'),
    path("new_game/", NewGame.as_view(), name="new_game"),
    path("game/<int:pk>/", WordleView.as_view(), name='game'),
    path("game/<int:pk>/check/", CheckGameState.as_view(), name = 'check'),
    path('history/', GameHistoryView.as_view(), name='history'),
]
