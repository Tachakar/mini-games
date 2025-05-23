from django.shortcuts import render
from .models import Word
def main(req):
    guesses = []
    for _ in range(6):
        guesses.append("abcde")

    ctx = {"guesses" : guesses}
    return render(req, "wordle/main.html", ctx)
