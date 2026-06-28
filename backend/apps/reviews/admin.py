from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Review


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = ("author_name", "rating", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "rating")
    search_fields = ("author_name", "text")
