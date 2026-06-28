from django.db import models


class Plan(models.Model):
    title = models.CharField("Назва", max_length=120)
    lessons_count = models.PositiveIntegerField("Кількість занять", default=1)
    price_per_lesson = models.PositiveIntegerField("Ціна за урок (грн)", default=0)
    total_price = models.PositiveIntegerField("Загальна вартість (грн)", default=0)

    is_speaking_club = models.BooleanField("Speaking Club", default=False)
    # List of features (strings) — mainly for the speaking club.
    features = models.JSONField("Переваги (список)", default=list, blank=True)

    note = models.CharField("Примітка", max_length=200, blank=True)
    is_highlighted = models.BooleanField("Виділити (популярний)", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифи"
        ordering = ("order", "id")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-calculate the total price if it was not set manually.
        if not self.total_price and self.price_per_lesson and self.lessons_count:
            self.total_price = self.price_per_lesson * self.lessons_count
        super().save(*args, **kwargs)
