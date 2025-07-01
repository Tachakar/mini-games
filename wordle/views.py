from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Word, Game
from random import choice
import json

NUMBER_OF_WORDS = 2315

class StartScreen(View, LoginRequiredMixin):
    template_name = 'wordle/index.html'
    def get(self, request):
        ctx = {'loged_in': request.user.is_authenticated}
        return render(request, self.template_name, ctx)

class WordleView(LoginRequiredMixin, TemplateView):

    template_name = 'wordle/game.html'
    MAX_GUESSES = 6
    MAX_WORD_LENGTH = 5

    def update_db(self, guesses: list[str], game_over: bool, won: bool, winning_word: str):
        game, created = Game.objects.get_or_create(
            defaults={'session_key': self.request.session.session_key, 'winning_word': winning_word, 'guesses': guesses, 'game_over':game_over, 'won': won}
        )
        if not created:
            game.guesses = guesses
            game.won = won
            game.game_over = game_over
        game.save()

    def start_game(self,winning_word):
        new_game = Game.objects.create(
            winning_word = winning_word, 
        )
        new_game.save()

    def init_session(self, request, winning_word):
        if "winning_word" not in request.session:
            request.session["winning_word"] = winning_word
        else:
            del request.session['winning_word']
        if "guesses" not in request.session:
            request.session["guesses"] = ["     " for _ in range(self.MAX_GUESSES)]
        else:
            del request.session['guesses']
        if "game_over" not in request.session:
            request.session["game_over"] = False
        else:
            del request.session['game_over']

    def get_random_word(self):
        words = Word.objects.values_list("text", flat = True)
        return str(choice(words))

    def get(self, request):
        winning_word = self.get_random_word()
        self.init_session(request, winning_word)
        self.start_game(winning_word)
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['winning_word'] = self.request.session.get("winning_word", "")
        data['guesses'] = self.request.session.get("guesses", ["     " for _ in range(self.MAX_GUESSES)])
        return data

    def post(self, request):
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
            self.update_db(guesses, game_over, won, winning_word)
            return JsonResponse({
                'status':'ok',
                'game_over': game_over,
                'guesses':guesses,
                'won':won,
                'winning_word': winning_word,
            },status=200)

        except:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong'},status=400)

