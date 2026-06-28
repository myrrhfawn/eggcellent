from rest_framework import generics
from rest_framework.response import Response

from apps.common import LangActivationMixin

from .models import Question
from .serializers import (
    QuestionSerializer,
    SubmitResultSerializer,
    SubmitSerializer,
)


class QuestionListView(LangActivationMixin, generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.filter(is_active=True).prefetch_related("answers")


class SubmitView(LangActivationMixin, generics.CreateAPIView):
    serializer_class = SubmitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        out = SubmitResultSerializer(submission, context=self.get_serializer_context())
        return Response(out.data)
