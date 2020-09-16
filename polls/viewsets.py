from django.shortcuts import get_list_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from .models import Poll, Question, Answer
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer

class PollViewSet(ListModelMixin, GenericViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    lookup_field = 'id'

    def list(self, *args, **kwargs):
        polls = get_list_or_404(Poll, stop__isnull=True)
        response_data = self.serializer_class(polls, many=True).data
        return Response(response_data, status=HTTP_200_OK)


class QuestionViewSet(ListModelMixin, GenericViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'poll_id'

    def list(self, request, *args, **kwargs):
        poll = self.request.GET.get(self.lookup_field, None)
        if not poll:
            return Response(f'No {self.lookup_field} provided', status=HTTP_400_BAD_REQUEST)

        questions = get_list_or_404(Question, poll__id=poll)
        response_data = self.serializer_class(questions, many=True).data
        return Response(response_data, status=HTTP_200_OK)


class AnswerViewSet(CreateModelMixin,
                    ListModelMixin,
                    GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    lookup_field = 'user_id'

    def list(self, *args, **kwargs):
        user = self.request.GET.get(self.lookup_field, None)
        if not user:
            return Response(f'No {self.lookup_field} provided', status=HTTP_400_BAD_REQUEST)
        answers = get_list_or_404(Answer, user_id=user)
        response_data = self.serializer_class(answers, many=True).data
        return Response(response_data, status=HTTP_200_OK)

    def create(self, *args, **kwargs):
        serializer = AnswerSerializer(data=self.request.data)
        if serializer.is_valid():
            if not self.request.session.session_key:
                self.request.session.create()
            session = self.request.session.session_key
            serializer.save(user_id=session)

            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

