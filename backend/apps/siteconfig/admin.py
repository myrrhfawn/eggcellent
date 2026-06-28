from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    fieldsets = (
        ("Hero-блок", {"fields": ("hero_title", "hero_subtitle")}),
        ("Соцмережі", {"fields": ("instagram_url", "telegram_url", "facebook_url")}),
        ("Контакти", {"fields": ("contact_phone", "contact_email")}),
        ("Ціни", {"fields": ("base_lesson_price",)}),
    )

    def has_add_permission(self, request):
        # Singleton — adding a new one is not allowed, only editing the existing one.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
