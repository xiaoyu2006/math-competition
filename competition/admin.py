from django.contrib import admin

from .models import Competition, Record, Problem, Answer

# Register your models here.
admin.site.register(Competition)
admin.site.register(Record)
admin.site.register(Problem)
admin.site.register(Answer)