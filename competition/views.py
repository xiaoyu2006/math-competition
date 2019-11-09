from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
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

@login_required
def comp_detail(request, comp_id):
    comp_obj = get_object_or_404(Competition, id=comp_id)
    context = {
        'comp': comp_obj,
        'probs': comp_obj.problem_set.all(),
        'registered': len(
            request.user.record_set.all().filter(competition__id=comp_id)
        ) == 1,
    }
    return render(request, 'competition/comp_detail.html', context)

@login_required
def prob_detail(request, prob_id):
    prob_obj = get_object_or_404(Problem, id=prob_id)
    context = {
        'comp': prob_obj.competition,
        'prob': prob_obj,
        'registered': len(
            request.user.record_set.all().filter(competition__id=prob_obj.competition.id)
        ) == 1,
    }
    return render(request, 'competition/prob_detail.html', context)

@login_required
def register_comp(request, comp_id):
    user = request.user
    q_set = user.record_set.all().filter(competition__id=comp_id)
    if len(q_set) == 0:
        comp = Competition.objects.get(id=comp_id)
        record = Record.objects.create(
            user=user,
            competition=comp,
            score=0
        )
        for problem in comp.problem_set.all():
            Answer.objects.create(
                record=record,
                problem=problem,
                user_answer=''
            )
    return HttpResponseRedirect(reverse('comp_detail', args=[comp_id]))