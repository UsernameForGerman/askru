from django.db import models
from django.contrib.auth import get_user_model

TEXT_ANSWER = 'Answer with text'
ONE_CHOICE = 'Answer with one choice'
MULTIPLE_CHOICE = 'Answer with multiple choice'

class Poll(models.Model):
    name = models.CharField(max_length=256)
    start = models.DateTimeField(auto_now_add=True)
    stop = models.DateTimeField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"<Poll(name={self.name}, description={self.description})>"

class Question(models.Model):
    TYPES = [
        (1, TEXT_ANSWER),
        (2, ONE_CHOICE),
        (3, MULTIPLE_CHOICE),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_text = models.TextField()
    type = models.IntegerField(choices=TYPES)

    def __str__(self):
        return f"<Question(poll={self.poll.name}, question={self.question_text}, type={self.type})>"

class Answer(models.Model):
    user_id = models.CharField(max_length=32)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"<Answer(user={self.user_id}, question={self.question.id}, answer={self.answer_text})>"



