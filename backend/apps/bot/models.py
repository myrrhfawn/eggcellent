from django.db import models


class TelegramAdmin(models.Model):
    """Chat IDs of users who passed /admin in the bot — notifications are sent to them."""

    chat_id = models.BigIntegerField("Chat ID", unique=True)
    username = models.CharField("Username", max_length=120, blank=True)
    is_active = models.BooleanField("Активний", default=True)
    created_at = models.DateTimeField("Додано", auto_now_add=True)

    class Meta:
        verbose_name = "Telegram-адмін"
        verbose_name_plural = "Telegram-адміни"
        ordering = ("-created_at",)

    def __str__(self):
        return self.username or str(self.chat_id)
