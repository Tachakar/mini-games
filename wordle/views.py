from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from .models import Word
from random import choice

NUMBER_OF_WORDS = 2315

class WordleView(TemplateView):

    model = Word
    template_name = 'wordle/main.html'

    def get_random_word(self):
        words = self.model.objects.values_list("text", flat = True)
        return choice(words)

    def get(self, request, *args, **kwargs):
        if 'winning_word' not in request.session:
            request.session['winning_word'] = self.get_random_word()
        if 'guesses' not in request.session:
            request.session['guesses'] = ['     ' for _ in range(6)]
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['winning_word'] = self.request.session['winning_word']
        data['guesses'] = self.request.session['guesses']
        return data

    def post(self, request, *args, **kwargs):
        guess = json.loads(request.body).get('guess')
        guesses = request.session.get("guesses", ["     " for _ in range(6)])
        row_index = 6
        for index, text in enumerate(guesses):
            if text == "     " and index < row_index :
                row_index = index

        if row_index < 6 and len(guess) == 5:
            guesses[row_index] = guess
            request.session['guesses'] = guesses
        if row_index >= 5:
            request.session['guesses'] = ['     ' for _ in range(6)]
            request.session['winning_word'] = self.get_random_word()
        return JsonResponse({"staus": "ok", "guesses": request.session['guesses']})
