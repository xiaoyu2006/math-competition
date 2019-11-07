from django.contrib import admin

from .models import Competition, Record, Problem, Answer

# Register your models here.
admin.register(Competition)
admin.register(Record)
admin.register(Problem)
admin.register(Answer)