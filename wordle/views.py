from django.core.exceptions import BadRequest
from django.db.models import Value
from django.http import JsonResponse
import json
from django.views.generic import TemplateView
from .models import Word
from random import choice

NUMBER_OF_WORDS = 2315

class WordleView(TemplateView):

    model = Word
    template_name = 'wordle/main.html'
    MAX_GUESSES = 6
    MAX_WORD_LENGHT = 5


    def initialize_session(self, request):
        if "winning_word" not in request.session:
            request.session["winning_word"] = self.get_random_word()
        if "guesses" not in request.session:
            request.session["guesses"] = ["     " for _ in range(self.MAX_GUESSES)]
        if "game_over" not in request.session:
            request.session["game_over"] = False

    def get_random_word(self):
        words = self.model.objects.values_list("text", flat = True)
        return str(choice(words))

    def get(self, request, *args, **kwargs):
        self.initialize_session(request)
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['winning_word'] = self.request.session.get("winning_word", "")
        data['guesses'] = self.request.session.get("guesses", ["     " for _ in range(self.MAX_GUESSES)])
        return data

    def post(self, request, *args, **kwargs):
        try:
            try:
                data = json.loads(request.body)
                guess = data.get('guess', '').lower()
            except:
                return JsonResponse({'status':'error', 'message': str(Exception)},status=400)

            if len(guess) != self.MAX_WORD_LENGHT:
                return JsonResponse({'status':'error', 'message': f'Word must be {self.MAX_WORD_LENGHT} letters long'},status =400)

            guesses = request.session.get("guesses",["     " for _ in range(self.MAX_GUESSES)])
            print(guesses)
            winning_word = request.session.get("winning_word", "")

            try:
                row_index = guesses.index("     ")
            except:
                return 

            guesses[row_index] = guess
            request.session["guesses"] = guesses

            won = guess == winning_word
            game_over = won or (row_index == self.MAX_GUESSES-1)
            request.sesssion['game_over'] = game_over

            print(row_index)
            return JsonResponse({"staus": "ok", "guesses": request.session['guesses'], 'game_over': game_over, 'won': won, 'winning_word': winning_word if game_over else None, 'row_index':row_index}, status=200)
        except:
            return JsonResponse({'status':'error', 'message':str(Exception)}, status=400)
