from django.shortcuts import get_list_or_404

from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin

from .models import Poll, Question, User, Answer
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer


class PollViewSet(ReadOnlyModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    lookup_field = 'id'


class QuestionViewSet(ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


class AnswerViewSet(CreateModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    lookup_field = 'user_id'

    def retrieve(self, *args, **kwargs):
        answers = get_list_or_404(Answer, user_id=kwargs.get(self.lookup_field))
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

