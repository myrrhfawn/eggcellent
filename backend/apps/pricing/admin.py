from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Plan


@admin.register(Plan)
class PlanAdmin(TranslationAdmin):
    list_display = (
        "title",
        "lessons_count",
        "price_per_lesson",
        "total_price",
        "is_speaking_club",
        "is_highlighted",
        "order",
        "is_active",
    )
    list_editable = ("order", "is_active", "is_highlighted")
    list_filter = ("is_active", "is_speaking_club")
    search_fields = ("title",)
    fields = (
        "title",
        "lessons_count",
        "price_per_lesson",
        "total_price",
        "is_speaking_club",
        "features",
        "note",
        "is_highlighted",
        "order",
        "is_active",
    )
