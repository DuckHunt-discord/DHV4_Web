from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, "public/index.jinja2")


def bot_commands(request):

    return render(request, "public/bot_commands.jinja2")
