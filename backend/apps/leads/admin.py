from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name", "phone", "channel", "source", "level", "is_processed", "created_at"
    )
    list_editable = ("is_processed",)
    list_filter = ("channel", "source", "is_processed", "level")
    search_fields = ("name", "phone")
    readonly_fields = (
        "channel", "source", "level", "submission", "answers", "created_at"
    )
