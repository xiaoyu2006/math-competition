from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label='Answer',max_length=100)