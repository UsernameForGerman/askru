from rest_framework.routers import DefaultRouter

from .viewsets import PollViewSet, AnswerViewSet, QuestionViewSet

router = DefaultRouter()
router.register('poll', PollViewSet)
router.register('answer', AnswerViewSet)
router.register('question', QuestionViewSet)
