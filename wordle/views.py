from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from .models import Word
from random import randint


NUMBER_OF_WORDS = 2315

class Main(TemplateView):

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        rand_id = randint(1,NUMBER_OF_WORDS)
        rand_word = get_object_or_404(Word, pk=rand_id)
        data["random_word"] = rand_word

        guesses = []
        for _ in range(6):
            guesses.append("     ")
        data["guesses"] = guesses

        return data

    def get(self, req):
        ctx = self.get_context_data()
        return render(req,"wordle/main.html", ctx)

