from django.shortcuts import render
def main(req):

    ctx = {}
    return render(req, "wordle/main.html", ctx)
