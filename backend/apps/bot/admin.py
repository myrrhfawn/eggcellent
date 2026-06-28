from django.contrib import admin

from .models import TelegramAdmin


@admin.register(TelegramAdmin)
class TelegramAdminAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "username", "is_active", "created_at")
    list_editable = ("is_active",)
    search_fields = ("username", "chat_id")
    readonly_fields = ("chat_id", "username", "created_at")
