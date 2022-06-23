from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from app.models import *

def auth(request):
    if request.method == 'POST':
        # NHJ9921gby-
        form = UserForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserForm()
    return render(request, 'auth.html', {'form': form})

@login_required(login_url='auth/')
def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', context={'books': books})