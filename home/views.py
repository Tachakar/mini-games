from django.shortcuts import redirect, render
from django.apps import apps
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import BaseUserCreationForm

def homepage(req):
    games = []
    for game in apps.get_app_configs():
        curr_game = game.name
        if curr_game.startswith('django.') or curr_game.startswith('crispy_') or curr_game == "home":
            continue
        else:
            games.append(curr_game)

    ctx = {"games":games}

    return render(req, "home/home_page.html", ctx)

class SignUp(TemplateView):
    template_name = 'home/sign_up.html'
    success_url = reverse_lazy('home:homepage')
    def get(self, request):
        form = BaseUserCreationForm
        ctx = {'form':form}
        return self.render_to_response(ctx)

    def post(self, request):
        username = request.POST.get('username', False)
        password1 = request.POST.get('password1', False)
        password2 = request.POST.get('password2', False)
        if username == False or password1 == False or password2 == False:
            #TODO PAGE REFRESH AND TRY AGAIN :)
            pass
        print(username,password1,password2)
        return redirect(self.success_url)


class Login(TemplateView):
    template_name = 'home/login.html'
    def get(self, request):
        ctx = {}
        return self.render_to_response(ctx)

    def post(self, request):
        pass

