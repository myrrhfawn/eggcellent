from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    """Singleton — global site settings (social networks, contacts, hero)."""

    # Hero
    hero_title = models.CharField("Заголовок hero", max_length=200, blank=True)
    hero_subtitle = models.CharField("Підзаголовок hero", max_length=300, blank=True)

    # Social networks
    instagram_url = models.URLField("Instagram", blank=True)
    telegram_url = models.URLField("Telegram", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)

    # Contacts
    contact_phone = models.CharField("Телефон", max_length=50, blank=True)
    contact_email = models.EmailField("Email", blank=True)

    # Base price of a single lesson (UAH) — for calculating the discount on plans
    base_lesson_price = models.PositiveIntegerField(
        "Базова ціна 1 уроку (грн)", default=400
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return "Налаштування сайту"

    def save(self, *args, **kwargs):
        # Always a single row.
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Do not allow deleting the singleton.
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def clean(self):
        if self.base_lesson_price <= 0:
            raise ValidationError({"base_lesson_price": "Має бути більше 0."})
