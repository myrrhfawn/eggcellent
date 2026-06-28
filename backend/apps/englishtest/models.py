from django.db import models


class Level(models.Model):
    """CEFR level with a score range (configured from the admin panel)."""

    code = models.CharField("Код (A1..C2)", max_length=10, unique=True)
    title = models.CharField("Назва", max_length=120)
    description = models.TextField("Опис", blank=True)
    min_score = models.PositiveIntegerField("Мін. балів", default=0)
    max_score = models.PositiveIntegerField("Макс. балів", default=0)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Рівень"
        verbose_name_plural = "Рівні (CEFR)"
        ordering = ("order", "min_score")

    def __str__(self):
        return f"{self.code} ({self.min_score}–{self.max_score})"

    @classmethod
    def for_score(cls, score: int):
        """Returns the level whose range contains the given score."""
        level = (
            cls.objects.filter(min_score__lte=score, max_score__gte=score)
            .order_by("order", "min_score")
            .first()
        )
        if level:
            return level
        # Fallback: the highest level whose threshold is exceeded, otherwise the lowest.
        below = cls.objects.filter(min_score__lte=score).order_by("-min_score").first()
        return below or cls.objects.order_by("order", "min_score").first()


class Question(models.Model):
    text = models.TextField("Питання")
    points = models.PositiveIntegerField("Балів за правильну відповідь", default=1)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активне", default=True)

    class Meta:
        verbose_name = "Питання"
        verbose_name_plural = "Питання тесту"
        ordering = ("order", "id")

    def __str__(self):
        return self.text[:60]


class Answer(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE,
        verbose_name="Питання",
    )
    text = models.CharField("Текст відповіді", max_length=300)
    is_correct = models.BooleanField("Правильна", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"
        ordering = ("order", "id")

    def __str__(self):
        return self.text


class TestSubmission(models.Model):
    """Stored result of a test attempt."""

    score = models.PositiveIntegerField("Набрано балів", default=0)
    max_score = models.PositiveIntegerField("Максимум балів", default=0)
    level = models.ForeignKey(
        Level, null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name="Рівень",
    )
    # {question_id: answer_id}
    answers = models.JSONField("Відповіді", default=dict, blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Проходження тесту"
        verbose_name_plural = "Проходження тесту"
        ordering = ("-created_at",)

    def __str__(self):
        lvl = self.level.code if self.level else "—"
        return f"{lvl}: {self.score}/{self.max_score}"
