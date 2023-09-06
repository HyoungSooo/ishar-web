from django.views.generic.list import ListView
from rest_framework import viewsets, permissions

from .models import Challenge
from .serializers import ChallengesSerializer


class ChallengesView(ListView):
    """
    Challenges view.
    """
    context_object_name = "challenges"
    model = Challenge
    queryset = model.objects.filter(
        is_active__exact=1
    ).order_by(
        "-is_active", "-winner_desc", "challenge_desc"
    ).all()
    template_name = "challenges.html.djt"


class ChallengesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows challenges to be viewed or edited.
    """
    model = Challenge
    permission_classes = [permissions.IsAdminUser]
    queryset = model.objects.all()
    serializer_class = ChallengesSerializer
