from rest_framework import serializers

from apps.englishtest.models import TestSubmission

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    submission_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Lead
        fields = ("id", "name", "phone", "source", "submission_id", "answers")
        read_only_fields = ("id",)

    def validate_phone(self, value):
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 9:
            raise serializers.ValidationError("Некоректний номер телефону.")
        return value

    def create(self, validated_data):
        submission_id = validated_data.pop("submission_id", None)
        submission = None
        if submission_id:
            submission = TestSubmission.objects.filter(id=submission_id).first()
        if submission:
            validated_data["submission"] = submission
            validated_data["level"] = submission.level
            validated_data.setdefault("source", Lead.Source.TEST)
            if not validated_data.get("answers"):
                validated_data["answers"] = submission.answers
        return super().create(validated_data)
