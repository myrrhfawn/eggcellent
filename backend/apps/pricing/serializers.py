from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    discount_percent = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            "id",
            "title",
            "lessons_count",
            "price_per_lesson",
            "total_price",
            "is_speaking_club",
            "features",
            "note",
            "is_highlighted",
            "discount_percent",
            "order",
        )

    def get_discount_percent(self, obj):
        """Discount relative to the base price of a single lesson (from SiteSettings)."""
        base = self.context.get("base_lesson_price") or 0
        if not base or obj.is_speaking_club or not obj.price_per_lesson:
            return 0
        if obj.price_per_lesson >= base:
            return 0
        return round((base - obj.price_per_lesson) / base * 100)
