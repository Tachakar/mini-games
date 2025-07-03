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
            game = Game.objects.get(pk=pk)
            print(game)
            winning_word = game.winning_word
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
                guesses = game.guesses
                row_index = guesses.index('     ')
            except:
                return JsonResponse({'status':'error', 'message': "Couldn't got row index"},status=400)

            guesses[row_index] = guessStatus
            won = guess == winning_word
            game_over = won or (row_index == MAX_WORD_LENGTH)
            try:
                Game.objects.filter(pk=pk).update(guesses=guesses, game_over=game_over, won=won)
            except: 
                return JsonResponse({'status':'error', 'message': "Couldn't update database."},status = 500)
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
