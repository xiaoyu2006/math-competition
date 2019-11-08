from django.shortcuts import render
from django.http import HttpResponse

from .models import Answer, Competition, Record, User, Problem

# Create your views here.
def index(request):
    context = {
        'comps': Competition.objects.order_by('-end_time'),
    }
    return render(request, 'competition/index.html', context=context)