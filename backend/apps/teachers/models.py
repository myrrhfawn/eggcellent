from django.db import models


class Teacher(models.Model):
    name = models.CharField("Ім'я", max_length=120)
    photo = models.ImageField("Фото", upload_to="teachers/")
    english_level = models.CharField("Рівень англійської", max_length=40)
    experience = models.CharField("Досвід", max_length=200, blank=True)
    bio = models.TextField("Опис", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"
        ordering = ("order", "id")

    def __str__(self):
        return self.name
