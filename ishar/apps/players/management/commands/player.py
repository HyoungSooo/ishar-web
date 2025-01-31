from pprint import pformat

from django.core.management.base import BaseCommand, CommandError

from ishar.apps.players.models import Player


class Command(BaseCommand):
    """player command to find single player."""

    help = "Find player."

    def add_arguments(self, parser):
        parser.add_argument("player", nargs=1, type=str)

    def handle(self, *args, **kwargs):

        player_name = kwargs["player"][0]

        try:
            player = Player.objects.get(name=player_name)
        except Player.DoesNotExist:
            raise CommandError('Player "%s" not found!' % player_name)

        self.stdout.write(self.style.SUCCESS(pformat(vars(player))))
        self.stdout.write(self.style.SUCCESS(player.account.__repr__()))
        self.stdout.write(self.style.SUCCESS(player.__repr__()))
