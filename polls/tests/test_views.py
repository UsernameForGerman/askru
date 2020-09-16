from django.urls import reverse
from django.conf import settings

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
import pytest
import typing
from importlib import import_module

from polls.viewsets import QuestionViewSet, AnswerViewSet, PollViewSet
from polls.models import Question, Answer, Poll
from polls.serializers import AnswerSerializer, PollSerializer, QuestionSerializer

user = 'test'

@pytest.fixture
def user() -> str:
    return 'test'

@pytest.fixture
def poll() -> Poll:
    return Poll.objects.create(name='1', description='test')

@pytest.fixture
def polls(poll: Poll) -> typing.List[Poll]:
    return [poll]

@pytest.fixture
def question(poll: Poll) -> Question:
    return Question.objects.create(poll=poll, question_text='test')

@pytest.fixture
def questions(question: Question) -> typing.List[Question]:
    return [question]

@pytest.fixture
def answers(questions: typing.List[Question], user: str) -> typing.List[Answer]:
    answers = list()
    for q in questions:
        answers.append(Answer.objects.create(question=q, answer_text='test', user_id=user))

    return answers

class TestPolls:
    factory = APIRequestFactory()

    @pytest.mark.django_db
    def test_list_polls(self, polls: typing.List[Poll]):
        path = reverse('polls:poll-list')
        request = self.factory.get(path)
        response = PollViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 200
        assert response.data == PollSerializer(polls, many=True).data

    @pytest.mark.django_db
    def test_empty_polls(self):
        path = reverse('polls:poll-list')
        request = self.factory.get(path)
        response = PollViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 404


class TestQuestions:
    factory = APIRequestFactory()

    @pytest.mark.django_db
    def test_list_questions(self, questions: typing.List[Question], poll: Poll):
        path = reverse('polls:question-list')
        request = self.factory.get(path, data={'poll_id': poll.id})
        response = QuestionViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 200
        assert response.data == QuestionSerializer(questions, many=True).data

        request = self.factory.get(path)
        response = QuestionViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 400

    @pytest.mark.django_db
    def test_empty_question(self, poll: Poll):
        path = reverse('polls:question-list')
        request = self.factory.get(path, data={'poll_id': poll.id})
        response = QuestionViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 404

class TestAnswers:
    factory = APIRequestFactory()
    client = APIClient()

    @pytest.mark.django_db
    def test_list_answer(self, answers: typing.List[Answer], user: str):
        path = reverse('polls:answer-list')
        request = self.factory.get(path, data={'user_id': user})
        response = AnswerViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 200
        assert response.data == AnswerSerializer(answers, many=True).data

        request = self.factory.get(path)
        response = AnswerViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 400

        request = self.factory.get(path, data={'user_id': f'Another_{user}'})
        response = AnswerViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_empty_answer(self, user: str):
        path = reverse('polls:answer-list')
        request = self.factory.get(path, data={'user_id': user})
        response = AnswerViewSet.as_view({'get': 'list'})(request)

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_create_answer(self, question: Question, user: str):
        path = reverse('polls:answer-list')
        request = self.factory.post(path)
        response = AnswerViewSet.as_view({'post': 'list'})(request)

        assert response.status_code == 400

        data = {
            'answer_text': 'test',
            'question': question.id,
        }
        request = self.factory.post(path, data=data)
        request.session = import_module(settings.SESSION_ENGINE).SessionStore(user)
        response = AnswerViewSet.as_view({'post': 'create'})(request)

        assert response.status_code == 200




