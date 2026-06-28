from rest_framework import generics

from apps.common import LangActivationMixin

from .models import Teacher
from .serializers import TeacherSerializer


class TeacherListView(LangActivationMixin, generics.ListAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.filter(is_active=True)
