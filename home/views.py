from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps

def homepage(req):
    games = []
    for game in apps.get_app_configs():
        curr_game = game.name
        if curr_game != "home" and curr_game.startswith("django.") == False:
            games.append(curr_game)

    ctx = {"games":games}

    return render(req, "home/home_page.html", ctx)

def login(req):
    return HttpResponse("Hello world")

def sign_up(req):
    return HttpResponse("Hello world")

