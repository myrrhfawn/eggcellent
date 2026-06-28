from rest_framework import serializers

from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            "hero_title",
            "hero_subtitle",
            "instagram_url",
            "telegram_url",
            "facebook_url",
            "contact_phone",
            "contact_email",
            "base_lesson_price",
        )
