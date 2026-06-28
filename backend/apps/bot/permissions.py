from django.conf import settings
from rest_framework.permissions import BasePermission


class HasBotSecret(BasePermission):
    """Allows only requests with the correct X-Bot-Secret header.

    A shared secret between the backend and the bot — so that third parties cannot
    call the bot endpoints.
    """

    message = "Invalid or missing bot secret."

    def has_permission(self, request, view):
        secret = settings.BOT_API_SECRET
        provided = request.headers.get("X-Bot-Secret", "")
        return bool(secret) and provided == secret
