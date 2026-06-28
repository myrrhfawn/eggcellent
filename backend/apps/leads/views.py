from rest_framework import generics

from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    serializer_class = LeadSerializer
    queryset = Lead.objects.all()
