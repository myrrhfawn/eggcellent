from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot"
    verbose_name = "Telegram-бот"

    def ready(self):
        # Connect the signal that notifies admins about new leads.
        from django.db.models.signals import post_save

        from apps.leads.models import Lead

        from .notify import notify_new_lead

        def _on_lead_created(sender, instance, created, **kwargs):
            if created:
                notify_new_lead(instance.channel)

        post_save.connect(
            _on_lead_created, sender=Lead, dispatch_uid="bot_notify_new_lead"
        )
