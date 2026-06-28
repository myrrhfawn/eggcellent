from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(TranslationAdmin):
    list_display = ("thumb", "name", "english_level", "order", "is_active")
    list_display_links = ("name",)
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

    @admin.display(description="Фото")
    def thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:42px;width:42px;'
                'object-fit:cover;border-radius:50%;" />',
                obj.photo.url,
            )
        return "—"
