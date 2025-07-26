from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Word, Game
from random import choice
import json

MAX_GUESSES = 6
MAX_WORD_LENGTH = 5
NUMBER_OF_WORDS = 2315
class Letter():
    def __init__(self, letter, status):
        self.letter = letter
        self.status = status

def get_random_word():
    words = Word.objects.values_list("text", flat = True)
    return str(choice(words))


class GameHistoryView(View, LoginRequiredMixin):
    template_name = 'wordle/history.html'
    def get(self, request):
        ctx = {}
        try:
            games = Game.objects.filter(user=request.user).order_by('-created_at')
            ctx['games'] = games
        except:
            print("User in not logged in")
        return render(request, self.template_name, ctx)


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
    def get(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        return JsonResponse({
            'winning_word': game.winning_word,
            'won': game.won,
            'game_over':game.game_over
        },status=200)

    def post(self, request, pk=None):
        try:
            data = json.loads(request.body)
            guess = data.get('guess').lower().strip()
            game = Game.objects.get(pk=pk)
            winning_word = game.winning_word
            statuses = game.statuses
            status = ''
            for i,letter in enumerate(guess):
                if letter == winning_word[i]:
                    status += 'c'
                elif letter != winning_word[i] and letter in winning_word:
                    status += 'i'
                else:
                    status += 'w'

            statuses.append(status)
            try:
                guesses = game.guesses
                row_index = guesses.index('     ')
                guesses[row_index]=guess
            except:
                return JsonResponse({'status':'error', 'message': "Couldn't got row index"},status=400)

            won = guess == winning_word
            game_over = won or (row_index == MAX_WORD_LENGTH)
            try:
                Game.objects.filter(pk=pk).update(guesses=guesses, game_over=game_over, won=won, statuses = statuses)
            except: 
                return JsonResponse({'status':'error', 'message': "Couldn't update database."},status = 500)
            return JsonResponse({
                'status':'ok',
                'game_over': game_over,
                'guesses':guesses,
                'status': status,
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


class WordleView(View, LoginRequiredMixin):

    template_name = 'wordle/game.html'
    def get(self, request, pk=None):
        ctx = {}
        game = get_object_or_404(Game, pk=pk)
        ctx['game_id'] = game.pk
        guesses = game.guesses
        winning_word = game.winning_word
        statuses = []
        for guess in guesses:
            x = []
            for i in range(MAX_WORD_LENGTH):
                if guess[i] == winning_word[i]:
                    x.append(Letter(guess[i], 'c'))
                elif guess[i] == ' ':
                    x.append(Letter(guess[i], 'e'))
                elif guess[i] not in winning_word:
                    x.append(Letter(guess[i], 'w'))
                else:
                    x.append(Letter(guess[i], 'i'))
            statuses.append(x)
        ctx['guesses'] = statuses

        return render(request, self.template_name, ctx)

