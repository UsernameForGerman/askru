from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Poll, Question, Answer, TEXT_ANSWER, MULTIPLE_CHOICE, ONE_CHOICE

class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    type = SerializerMethodField()
    poll = SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_type(self, question):
        return question.get_type_display()

    def get_poll(self, question):
        return question.poll.name

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('user_id', )
    #
    # def save(self, **kwargs):
    #     print(kwargs)
    #     return Answer.objects.create(user_id=kwargs['user_id'], **kwargs)
