from django.urls import reverse, resolve
from django.utils.timezone import now

import pytest

from polls.models import Poll, Question, Answer

POLL = 1
USER = 'test'

def test_poll_urls():
    assert reverse('polls:poll-list') == "/api/v1/poll/"
    assert resolve("/api/v1/poll/").view_name == "polls:poll-list"

def test_question_urls():
    assert reverse('polls:question-list') == "/api/v1/question/"
    assert resolve("/api/v1/question/").view_name == "polls:question-list"

def test_answer_urls():
    assert reverse('polls:answer-list') == "/api/v1/answer/"
    assert resolve("/api/v1/answer/").view_name == "polls:answer-list"

