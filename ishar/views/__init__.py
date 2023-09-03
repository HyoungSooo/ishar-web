from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView

from ishar.apps.news.models import News


class ConnectRedirectView(RedirectView):
    permanent = True
    url = settings.CONNECT_URL


class HistoryView(TemplateView):
    template_name = "history.html.djt"


class PortalView(TemplateView):
    template_name = "portal.html.djt"


class StartView(TemplateView):
    template_name = "start.html.djt"


class SupportView(TemplateView):
    template_name = "support.html.djt"


class WelcomeView(TemplateView):
    template_name = "welcome.html.djt"
    extra_context = {"news": News.objects.all()}
