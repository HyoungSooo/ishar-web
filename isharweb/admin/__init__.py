from django.contrib import admin
from django.contrib.auth.admin import Group

from .account import AccountAdmin
from .account.upgrade import AccountUpgradeAdmin
from .challenge import ChallengeAdmin
from .force import ForceAdmin
from .news import NewsAdmin
from .player import ClassAdmin, PlayerAdmin
from .quest import QuestAdmin, QuestStepAdmin
from .race import RaceAdmin
from .season import SeasonAdmin
from .spell import SpellAdmin

from ..models.account import Account
from ..models.account.upgrade import AccountUpgrade
from ..models.challenge import Challenge
from ..models.force import Force
from ..models.news import News
from ..models.player import Player, Class
from ..models.quest import Quest
from ..models.quest.step import QuestStep
from ..models.race import Race
from ..models.season import Season
from ..models.spell import Spell


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountUpgrade, AccountUpgradeAdmin)

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Force, ForceAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Player, PlayerAdmin)

admin.site.register(Quest, QuestAdmin)
admin.site.register(QuestStep, QuestStepAdmin)

admin.site.register(Race, RaceAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Spell, SpellAdmin)

# Disable "groups" in /admin/
admin.site.unregister(Group)
