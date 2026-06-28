from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.leads.models import Lead

from .models import TelegramAdmin
from .permissions import HasBotSecret
from .serializers import BotLeadCreateSerializer, BotLeadListSerializer


class BotAuthView(APIView):
    """Verifies the /admin password in the bot and registers the admin's chat_id."""

    permission_classes = [HasBotSecret]

    def post(self, request):
        password = request.data.get("password", "")
        chat_id = request.data.get("chat_id")
        username = request.data.get("username", "")
        if chat_id is None:
            return Response({"detail": "chat_id required"}, status=400)

        if not settings.BOT_ADMIN_PASSWORD or password != settings.BOT_ADMIN_PASSWORD:
            return Response({"ok": False})

        TelegramAdmin.objects.update_or_create(
            chat_id=chat_id,
            defaults={"username": username or "", "is_active": True},
        )
        return Response({"ok": True})


class BotLeadCreateView(APIView):
    """Creating a lead from the bot."""

    permission_classes = [HasBotSecret]

    def post(self, request):
        serializer = BotLeadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        return Response(
            {
                "ok": True,
                "id": lead.id,
                "level": lead.level.code if lead.level else None,
            }
        )


class BotLeadListView(ListAPIView):
    """List of leads for the bot admin (only if chat_id is a registered admin)."""

    permission_classes = [HasBotSecret]
    serializer_class = BotLeadListSerializer

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        if not chat_id or not TelegramAdmin.objects.filter(
            chat_id=chat_id, is_active=True
        ).exists():
            return Lead.objects.none()
        return Lead.objects.all()[:20]
