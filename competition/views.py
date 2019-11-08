from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Answer, Competition, Record, User, Problem

# Create your views here.
def index(request):
    context = {
        'comps': Competition.objects.order_by('-end_time'),
        'now': datetime.now(),
    }
    return render(request, 'competition/index.html', context)

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(
                request=request,
                username=new_user.username,
                password=request.POST['password1'],
            )
            login(request, auth_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
    }
    return render(request, 'competition/register.html', context)

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def log_in(request):
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
    }
    return render(request, 'competition/login.html', context)