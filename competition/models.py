from django.db import models
from django.contrib.auth.models import User

# COMPETITION
class Competition(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

# One PROBLEM of a COMPETITION
class Problem(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    score = models.FloatField()
    right_answer = models.CharField(max_length=100)

# A RECORD of a COMPETITION
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    score = models.FloatField()

# An ANSWER of a PROBLEM
class Answer(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100)