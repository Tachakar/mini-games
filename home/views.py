from django.shortcuts import render
from django.apps import apps
from django.contrib.auth.models import User
from django.views.generic import TemplateView

def homepage(req):
    games = []
    for game in apps.get_app_configs():
        curr_game = game.name
        if curr_game != "home" and curr_game.startswith("django.") == False:
            games.append(curr_game)

    ctx = {"games":games}

    return render(req, "home/home_page.html", ctx)

class SignUp(TemplateView):
    template_name = 'home/sign_up.html'
    def get(self, request):
        ctx = {}
        return self.render_to_response(ctx)

    def post(self, request):
        pass

class Login(TemplateView):
    template_name = 'home/login.html'
    def get(self, request):
        ctx = {}
        return self.render_to_response(ctx)

    def post(self, request):
        pass

