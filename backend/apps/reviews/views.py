from rest_framework import generics

from apps.common import LangActivationMixin

from .models import Review
from .serializers import ReviewSerializer


class ReviewListView(LangActivationMixin, generics.ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(is_active=True)
