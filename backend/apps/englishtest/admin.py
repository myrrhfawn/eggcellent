from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import Answer, Level, Question, TestSubmission


@admin.register(Level)
class LevelAdmin(TranslationAdmin):
    list_display = ("code", "title", "min_score", "max_score", "order")
    list_editable = ("min_score", "max_score", "order")
    ordering = ("order",)


class AnswerInline(TranslationTabularInline):
    model = Answer
    extra = 4
    fields = ("text", "is_correct", "order")


@admin.register(Question)
class QuestionAdmin(TranslationAdmin):
    list_display = ("__str__", "points", "order", "is_active")
    list_editable = ("points", "order", "is_active")
    list_filter = ("is_active",)
    inlines = [AnswerInline]


@admin.register(TestSubmission)
class TestSubmissionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "level", "score", "max_score")
    list_filter = ("level",)
    readonly_fields = ("score", "max_score", "level", "answers", "created_at")

    def has_add_permission(self, request):
        return False
