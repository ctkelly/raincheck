from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:all')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


