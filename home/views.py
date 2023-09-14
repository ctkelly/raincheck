from django.shortcuts import render
import requests


def index(request):
    template_name = 'home/main.html'
    url = 'https://catfact.ninja/fact'
    response = requests.get(url)
    cat_fact = response.json()
    ctx = {'fact': cat_fact['fact']}

    return render(request, template_name, ctx)
