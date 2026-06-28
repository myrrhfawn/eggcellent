from rest_framework import generics

from apps.common import LangActivationMixin
from apps.siteconfig.models import SiteSettings

from .models import Plan
from .serializers import PlanSerializer


class PlanListView(LangActivationMixin, generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["base_lesson_price"] = SiteSettings.load().base_lesson_price
        return ctx
