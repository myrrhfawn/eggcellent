from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    author_name = models.CharField("Ім'я", max_length=120)
    text = models.TextField("Відгук")
    rating = models.PositiveSmallIntegerField(
        "Оцінка",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ("order", "-id")

    def __str__(self):
        return f"{self.author_name} ({self.rating}★)"
