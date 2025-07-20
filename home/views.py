from django.shortcuts import redirect, render
from django.apps import apps
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

def homepage(request):
    games = []
    template_name = "home/home_page.html"
    for game in apps.get_app_configs():
        curr_game = game.name
        if curr_game.startswith('django.') or curr_game.startswith('crispy_') or curr_game == "home":
            continue
        else:
            games.append(curr_game)

    ctx = {"games":games}

    return render(request, template_name, ctx)

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home:homepage'))

class SignUp(TemplateView):
    template_name = 'home/sign_up.html'
    success_url = reverse_lazy('home:homepage')
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        ctx = {'form':form}
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        user_form = UserCreationForm(request.POST)
        ctx = {}
        if not user_form.is_valid():
            ctx['errors'] = user_form.errors
            return render(request, 'home/fail.html', ctx)
        user_form.save()
        return redirect(self.success_url)


class Login(TemplateView):
    template_name = 'home/login.html'
    def get(self, request):
        ctx = {}
        return self.render_to_response(ctx)

    def post(self, request):
        pass

