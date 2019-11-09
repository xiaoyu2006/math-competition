from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Answer, Competition, Record, User, Problem

from .forms import AnswerForm, CompForm, ProbForm



# Views for user manaegment.

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





# Views for other pages:

def index(request):
    context = {
        'comps': Competition.objects.order_by('-end_time'),
        'now': timezone.now(),
    }
    return render(request, 'competition/index.html', context)

@login_required
def comp_detail(request, comp_id):
    comp_obj = get_object_or_404(Competition, id=comp_id)
    is_registered = len(
        request.user.record_set.all().filter(competition__id=comp_obj.id)
    ) == 1
    context = {
        'comp': comp_obj,
        'probs': comp_obj.problem_set.all(),
        'registered': is_registered,
        'now': timezone.now(),
        'user': request.user,
    }
    if is_registered:
        rec_obj = Record.objects.filter(
            user__id=request.user.id,
            competition__id=comp_obj.id,
        ).all()[0]
        context['record'] = rec_obj
    return render(request, 'competition/comp_detail.html', context)

@login_required
def prob_detail(request, prob_id):
    prob_obj = get_object_or_404(Problem, id=prob_id)
    is_registered = len(
            request.user.record_set.all().filter(competition__id=prob_obj.competition.id)
        ) == 1
    context = {
        'comp': prob_obj.competition,
        'prob': prob_obj,
        'registered': is_registered,
        'now': timezone.now(),
    }
    if is_registered:
        rec_obj = Record.objects.filter(
            user__id=request.user.id,
            competition__id=prob_obj.competition.id,
        ).all()[0]
        ans_obj = Answer.objects.filter(
            record__id=rec_obj.id,
            problem__id=prob_obj.id,
        ).all()[0]
    if is_registered:
        if request.method != 'POST':
            form = AnswerForm(
                initial={'answer': ans_obj.user_answer}
            )
            context['answer'] = ans_obj
        else:
            form = AnswerForm(data=request.POST)
            if form.is_valid():
                if ans_obj.user_answer != form.cleaned_data['answer']:
                    if form.cleaned_data['answer'] == prob_obj.right_answer:
                        rec_obj.score += prob_obj.score
                        ans_obj.user_answer = form.cleaned_data['answer']
                        ans_obj.save()
                        rec_obj.save()
                    else:
                        if ans_obj.user_answer == prob_obj.right_answer:
                            rec_obj.score -= prob_obj.score
                            ans_obj.user_answer = form.cleaned_data['answer']
                            ans_obj.save()
                            rec_obj.save()
        context['form'] = form
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

@login_required
def standings(request, comp_id):
    comp_obj = get_object_or_404(Competition, id=comp_id)
    records = comp_obj.record_set.order_by('score')
    context = {
        'records': records,
        'comp': comp_obj,
        'now': timezone.now(),
    }
    return render(request, 'competition/comp_standings.html', context)

@login_required
def new_comp(request):
    if request.method != 'POST':
        form = CompForm()
    else:
        form = CompForm(data=request.POST)
        if form.is_valid():
            new_comp = Competition.objects.create(
                auther=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )
            new_comp.save()
            return HttpResponseRedirect(reverse('comp_detail', args=[new_comp.id]))
    context = {
        'form': form,
    }
    return render(request, 'competition/new_comp.html', context)

@login_required
def new_prob(request, comp_id):
    comp_obj = get_object_or_404(Competition, id=comp_id)
    if request.method != 'POST':
        form = ProbForm()
    else:
        if request.user.id == comp_obj.auther.id:
            form = ProbForm(data=request.POST)
            if form.is_valid():
                new_prob = Problem.objects.create(
                    competition=comp_obj,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    score=form.cleaned_data['score'],
                    right_answer=form.cleaned_data['answer'],
                )
                new_prob.save()
                return HttpResponseRedirect(reverse('prob_detail', args=[new_prob.id]))
        else:
            return HttpResponseForbidden(
                "Sorry but you have no access to add a problem into this competition."
            )
    context = {
        'comp': comp_obj,
        'user': request.user,
        'form': form,
    }
    return render(request, 'competition/new_prob.html', context)