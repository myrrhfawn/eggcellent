from rest_framework import serializers

from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Teacher
        fields = ("id", "name", "photo", "english_level", "experience", "bio", "order")
