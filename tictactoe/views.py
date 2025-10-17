from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

class TictactoeStartScreen(View, LoginRequiredMixin):
    template_name = "tictactoe/index.html"
    def get(self, request):
        return render(request, self.template_name, {})
