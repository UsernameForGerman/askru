from django.db import models
from django.contrib.auth import get_user_model

TEXT_ANSWER = 'Answer with text'
ONE_CHOICE = 'Answer with one choice'
MULTIPLE_CHOICE = 'Answer with multiple choice'

User = get_user_model()

class Poll(models.Model):
    name = models.CharField(max_length=256)
    start = models.DateTimeField(auto_now_add=True)
    stop = models.DateTimeField(auto_now=True)
    description = models.TextField()

class Question(models.Model):
    TYPES = [
        (1, TEXT_ANSWER),
        (2, ONE_CHOICE),
        (3, MULTIPLE_CHOICE),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.IntegerField(choices=TYPES)



