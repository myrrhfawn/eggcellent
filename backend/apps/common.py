"""Shared utilities for the API."""
from django.conf import settings
from django.utils import translation

SUPPORTED_LANGS = {code for code, _ in settings.LANGUAGES}


class LangActivationMixin:
    """Activates the language from ?lang=uk|en for DRF views.

    modeltranslation returns fields for the active language, so it is enough
    to activate it before serialization.
    """

    def initial(self, request, *args, **kwargs):
        lang = request.query_params.get("lang")
        if lang in SUPPORTED_LANGS:
            translation.activate(lang)
        super().initial(request, *args, **kwargs)
