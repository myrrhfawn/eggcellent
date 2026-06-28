"""Aggregator of the public API under /api/."""
from django.urls import path

from apps.bot.views import BotAuthView, BotLeadCreateView, BotLeadListView
from apps.englishtest.views import QuestionListView, SubmitView
from apps.leads.views import LeadCreateView
from apps.pricing.views import PlanListView
from apps.reviews.views import ReviewListView
from apps.siteconfig.views import SiteSettingsView
from apps.teachers.views import TeacherListView

urlpatterns = [
    path("site-settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("reviews/", ReviewListView.as_view(), name="reviews"),
    path("plans/", PlanListView.as_view(), name="plans"),
    path("test/questions/", QuestionListView.as_view(), name="test-questions"),
    path("test/submit/", SubmitView.as_view(), name="test-submit"),
    path("leads/", LeadCreateView.as_view(), name="leads"),
    # --- Bot (protected by X-Bot-Secret) ---
    path("bot/auth/", BotAuthView.as_view(), name="bot-auth"),
    path("bot/leads/", BotLeadCreateView.as_view(), name="bot-lead-create"),
    path("bot/leads/list/", BotLeadListView.as_view(), name="bot-lead-list"),
]
