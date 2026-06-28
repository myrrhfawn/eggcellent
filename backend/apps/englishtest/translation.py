from modeltranslation.translator import TranslationOptions, register

from .models import Answer, Level, Question


@register(Level)
class LevelTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ("text",)
