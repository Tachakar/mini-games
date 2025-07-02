from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Word, Game
from random import choice
import json

MAX_GUESSES = 6
MAX_WORD_LENGTH = 5
NUMBER_OF_WORDS = 2315
def get_random_word():
    words = Word.objects.values_list("text", flat = True)
    return str(choice(words))
def update_db(guesses: list[str], game_over: bool, won: bool, winning_word: str):
        game, created = Game.objects.get_or_create(
            defaults={'winning_word': winning_word, 'guesses': guesses, 'game_over':game_over, 'won': won}
        )
        if not created:
            game.guesses = guesses
            game.won = won
            game.game_over = game_over
        game.save()

class NewGame(LoginRequiredMixin, View):
    def post(self,request):

        game = Game.objects.create(
            winning_word = get_random_word(), 
            guesses = ['     ' for _ in range(MAX_GUESSES)],
            user = request.user,
            game_over = False,
            won = False,
        )
        return redirect('wordle:game', pk=game.pk)

class CheckGameState(View, LoginRequiredMixin):
    def post(self, request, pk=None):
        try:
            data = json.loads(request.body)
            guess = data.get('guess').lower().strip()
            game = get_object_or_404(Game, pk=pk, user = request.user)
            print(game)
            winning_word = game.winning_word
            guesses = game.guesses
            guessStatus = {}
            for i,letter in enumerate(guess):
                if letter == winning_word[i]:
                    n = {'letter': letter, 'status': 'correct'}
                elif letter != winning_word[i] and letter in winning_word:
                    n = {'letter': letter, 'status': 'inside'}
                else:
                    n = {'letter': letter, 'status': 'wrong'}
                guessStatus[i] = n

            try:
                row_index = guesses.index('     ')
            except:
                return JsonResponse({'status':'error', 'message': "Couldn't got row index"},status=400)

            guesses[row_index] = guessStatus
            won = guess == winning_word
            game_over = False
            game_over = won or (row_index == MAX_WORD_LENGTH)
            update_db(guesses, game_over, won, winning_word)
            return JsonResponse({
                'status':'ok',
                'game_over': game_over,
                'guesses':guesses,
                'won':won,
                'winning_word': winning_word,
            },status=200)

        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON'},
                status=400
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {'status': 'error', 'message': 'Internal server error'},
                status=500
            )

class StartScreen(View, LoginRequiredMixin):
    template_name = 'wordle/index.html'
    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)

class WordleView(TemplateView, LoginRequiredMixin):

    template_name = 'wordle/game.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        game_id = self.kwargs.get('pk')
        data['guesses'] = ['     ' for _ in range(MAX_GUESSES)]
        data['game_id'] = game_id
        return data
    
    def get(self, request, pk=None):
        ctx = self.get_context_data()
        return self.render_to_response(ctx)
