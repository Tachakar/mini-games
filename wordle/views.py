import json
from django.http import JsonResponse
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
        guesses = request.session['guesses']
        row_index = None
        for index, text in enumerate(request.session['guesses']):
            if text == "     ":
                row_index = index
                break
        if row_index is not None and guess is not None:
            if len(guess) == 5:
                guesses[row_index] = guess
            request.session['guesses'] = guesses
        else:
            del request.session['guesses']
            del request.session['winning_word']
        return JsonResponse({'status': 'ok' })
