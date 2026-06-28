from rest_framework import serializers

from apps.englishtest.models import TestSubmission
from apps.leads.models import Lead


class BotLeadCreateSerializer(serializers.Serializer):
    """Creating a lead from the bot (channel = bot)."""

    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=40)
    submission_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated):
        sub = None
        sid = validated.get("submission_id")
        if sid:
            sub = TestSubmission.objects.filter(id=sid).first()
        return Lead.objects.create(
            name=validated["name"],
            phone=validated["phone"],
            channel=Lead.Channel.BOT,
            source=Lead.Source.TEST if sub else Lead.Source.FORM,
            submission=sub,
            level=sub.level if sub else None,
            answers=sub.answers if sub else {},
        )


class BotLeadListSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source="level.code", default=None)

    class Meta:
        model = Lead
        fields = (
            "id",
            "name",
            "phone",
            "source",
            "channel",
            "level",
            "is_processed",
            "created_at",
        )
