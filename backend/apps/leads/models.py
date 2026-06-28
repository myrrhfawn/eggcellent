from django.db import models


class Lead(models.Model):
    class Source(models.TextChoices):
        TEST = "test", "Через тест"
        FORM = "form", "Через форму"

    class Channel(models.TextChoices):
        SITE = "site", "Сайт"
        BOT = "bot", "Telegram-бот"

    name = models.CharField("Ім'я", max_length=120)
    phone = models.CharField("Телефон", max_length=40)
    source = models.CharField(
        "Джерело", max_length=10, choices=Source.choices, default=Source.FORM
    )
    channel = models.CharField(
        "Канал", max_length=10, choices=Channel.choices, default=Channel.SITE
    )
    level = models.ForeignKey(
        "englishtest.Level",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Рівень (з тесту)",
    )
    submission = models.ForeignKey(
        "englishtest.TestSubmission",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Проходження тесту",
    )
    # Optional — a copy of the test answers.
    answers = models.JSONField("Відповіді тесту", default=dict, blank=True)
    is_processed = models.BooleanField("Опрацьовано", default=False)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.phone}"
