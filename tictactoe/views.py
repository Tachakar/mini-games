from django.shortcuts import render
from django.views.generic import View

class Index(View):
    template_name = "tictactoe/index.html"
    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)
