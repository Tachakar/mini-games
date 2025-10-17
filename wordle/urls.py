from django.urls import path
from .views import WordleView, WordleStartScreen, WordleNewGame, WordleCheckGameState, WordleGameHistoryView
app_name = "wordle"

urlpatterns = [
    path("", WordleStartScreen.as_view(), name='index'),
    path("new_game/", WordleNewGame.as_view(), name="new_game"),
    path("game/<int:pk>/", WordleView.as_view(), name='game'),
    path("game/<int:pk>/check/", WordleCheckGameState.as_view(), name = 'check'),
    path('history/', WordleGameHistoryView.as_view(), name='history'),
]
