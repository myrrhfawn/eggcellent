from rest_framework import serializers

from .models import Answer, Level, Question, TestSubmission


class AnswerPublicSerializer(serializers.ModelSerializer):
    """Public answer — WITHOUT the is_correct field (so as not to reveal the correct one)."""

    class Meta:
        model = Answer
        fields = ("id", "text")


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "points", "answers")


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ("id", "code", "title", "description", "min_score", "max_score")


class SubmitSerializer(serializers.Serializer):
    """Input: {answers: {question_id: answer_id, ...}}"""

    answers = serializers.DictField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def create(self, validated_data):
        raw = validated_data["answers"]
        # Normalize the keys to int.
        chosen = {int(qid): int(aid) for qid, aid in raw.items()}

        questions = Question.objects.filter(is_active=True).prefetch_related("answers")
        score = 0
        max_score = 0
        for q in questions:
            max_score += q.points
            picked = chosen.get(q.id)
            if picked is None:
                continue
            ans = next((a for a in q.answers.all() if a.id == picked), None)
            if ans and ans.is_correct:
                score += q.points

        level = Level.for_score(score)
        submission = TestSubmission.objects.create(
            score=score,
            max_score=max_score,
            level=level,
            answers={str(k): v for k, v in chosen.items()},
        )
        return submission


class SubmitResultSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)

    class Meta:
        model = TestSubmission
        fields = ("id", "score", "max_score", "level")
