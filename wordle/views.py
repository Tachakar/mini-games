from django.http import JsonResponse
import json
from django.views.generic import TemplateView
from .models import Word, Game
from random import choice

NUMBER_OF_WORDS = 2315

class WordleView(TemplateView):

    template_name = 'wordle/main.html'
    MAX_GUESSES = 6
    MAX_WORD_LENGTH = 5

    def update_db(self, reqeust, guesses: list[str], game_over: bool, won: bool, winning_word: str):
        game, created = Game.objects.get_or_create(
            session_key = self.request.session.session_key, 
            defaults={'session_key': self.request.session.session_key, 'winning_word': winning_word, 'guesses': guesses, 'game_over':game_over, 'won': won}
        )
        if not created:
            game.guesses = guesses
            game.won = won
            game.game_over = game_over
        game.save()

    def init_session(self, request):
        if "winning_word" not in request.session:
            request.session["winning_word"] = self.get_random_word()
        if "guesses" not in request.session:
            request.session["guesses"] = ["     " for _ in range(self.MAX_GUESSES)]
        if "game_over" not in request.session:
            request.session["game_over"] = False

    def get_random_word(self):
        words = Word.objects.values_list("text", flat = True)
        return str(choice(words))

    def get(self, request, *args, **kwargs):
        if 'guesses' in request.session:
            del request.session['guesses']
        if 'winning_word' in request.session:
            del request.session['winning_word']
        if 'game_over' in request.session:
            del request.session['game_over']
        self.init_session(request)
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['winning_word'] = self.request.session.get("winning_word", "")
        data['guesses'] = self.request.session.get("guesses", ["     " for _ in range(self.MAX_GUESSES)])
        return data

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            guess = data.get('guess').lower().strip()
            winning_word = request.session.get('winning_word', '')
            guessStatus = {}
            for i,letter in enumerate(guess):
                if letter == winning_word[i]:
                    n = {'letter': letter, 'status': 'correct'}
                elif letter != winning_word[i] and letter in winning_word:
                    n = {'letter': letter, 'status': 'inside'}
                else:
                    n = {'letter': letter, 'status': 'wrong'}
                guessStatus[i] = n

            guesses = request.session.get('guesses', ['     ' for _ in range(self.MAX_GUESSES)])
            try:
                row_index = guesses.index('     ')
            except:
                return JsonResponse({'status':'error', 'message': "Couldn't got row index"},status=400)

            guesses[row_index] = guessStatus
            request.session['guesses'] = guesses
            won = guess == winning_word
            game_over = won or (row_index == self.MAX_WORD_LENGTH)
            request.session['game_over'] = game_over
            #self.update_db(request, guesses, game_over, won, winning_word)
            return JsonResponse({
                'status':'ok',
                'game_over': game_over,
                'guesses':guesses,
                'won':won,
                'winning_word': winning_word if game_over else '',
            },status=200)

        except:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong'},status=400)

