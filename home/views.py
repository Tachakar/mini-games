from django.shortcuts import render
from django.apps import apps
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import BaseUserCreationForm

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
    success_url = reverse_lazy('homepage')
    def get(self, request):
        form = BaseUserCreationForm
        ctx = {'form':form}
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

