from django import forms

from django.utils import timezone

class AnswerForm(forms.Form):
    answer = forms.CharField(label='Answer',max_length=100)

class CompForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=1000)
    start_time = forms.DateTimeField(label='Start time', initial=timezone.now())
    end_time = forms.DateTimeField(label='Deadline', initial=timezone.now())

class ProbForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=1000, widget=forms.Textarea(attrs={'rows': 30}))
    answer = forms.CharField(label='Answer', max_length=100)
    score = forms.FloatField(label_suffix='Score')
