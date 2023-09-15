from django.contrib import admin
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from ..accounts.models import Account
from ...util.ip import dec2ip
from ...util.level import get_immortal_level, get_immortal_type


class Player(models.Model):
    """
    Player character.
    """
    account = models.ForeignKey(
        to=Account,
        on_delete=models.CASCADE,
        related_query_name="player",
        related_name="players",
        help_text="Account that owns the player character.",
        verbose_name="Account"
    )
    name = models.SlugField(
        unique=True,
        max_length=15,
        help_text="Name of the player character.",
        verbose_name="Name"
    )
    create_ident = models.CharField(
        max_length=10,
        help_text="Ident that created the player.",
        verbose_name="Create IDENT"
    )
    last_isp = models.CharField(
        max_length=30,
        help_text="Last Internet Service Provider (ISP) to join as the player.",
        verbose_name="Create IDENT"
    )
    description = models.CharField(
        max_length=240, blank=True, null=True,
        help_text="User-written in-game player description.",
        verbose_name="Description"
    )
    title = models.CharField(
        max_length=45,
        help_text="User-selectable player title.",
        verbose_name="Title"
    )
    poofin = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof in.",
        verbose_name="Poof In"
    )
    poofout = models.CharField(
        max_length=80,
        help_text="String displayed upon player poof out.",
        verbose_name="Poof In"
    )
    bankacc = models.PositiveIntegerField(
        help_text="Bank account balance.",
        verbose_name="Bank Account"
    )
    logon_delay = models.PositiveSmallIntegerField(
        help_text="Delay when logging on.",
        verbose_name="Logon Delay"
    )
    true_level = models.PositiveIntegerField(
        help_text="True level of the player character.",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=max(settings.IMMORTAL_LEVELS)[0])
        ],
        verbose_name="True Level"
    )
    renown = models.PositiveIntegerField(
        help_text="Amount of renown available for the player to spend.",
        verbose_name="Renown"
    )
    remorts = models.PositiveIntegerField(
        help_text="Number of times that the player has remorted.",
        verbose_name="Remorts"
    )
    favors = models.PositiveIntegerField(
        help_text="Amount of favors for the player.",
        verbose_name="Favors"
    )
    online = models.IntegerField(
        blank=True,
        null=True,
        help_text="Amount of time spent logged in to the game, in seconds.",
        verbose_name="Online"
    )
    bound_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is bound.",
        verbose_name="Bound Room"
    )
    load_room = models.PositiveIntegerField(
        help_text="Room ID number where the player is loaded.",
        verbose_name="Load Room"
    )
    invstart_level = models.IntegerField(
        blank=True,
        null=True,
        help_text="Invisible Start Level.",
        verbose_name="Invisible Start Level"
    )
    login_failures = models.PositiveSmallIntegerField(
        help_text="Number of login failures.",
        verbose_name="Login Failures"
    )
    create_haddr = models.IntegerField(
        help_text="HADDR that created the player.",
        verbose_name="Create HADDR"
    )
    login_fail_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="HADDR that last failed to log in to the player.",
        verbose_name="Login Fail HADDR"
    )
    last_haddr = models.IntegerField(
        blank=True,
        null=True,
        help_text="Last HADDR to join as the player.",
        verbose_name="Last HADDR"
    )
    last_ident = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Last ident to join as the player.",
        verbose_name="Last IDENT"
    )
    load_room_next = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next.",
        verbose_name="Load Room Next"
    )
    load_room_next_expires = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Load Room Next Expires.",
        verbose_name="Load Room Next Expires"
    )
    aggro_until = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Aggro Until.",
        verbose_name="Aggro Until"
    )
    inn_limit = models.PositiveSmallIntegerField(
        help_text="Inn Limit.",
        verbose_name="Inn Limit"
    )
    held_xp = models.IntegerField(
        blank=True,
        null=True,
        help_text="Held XP.",
        verbose_name="Held XP"
    )
    last_isp_change = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Last Internet Service Provider (ISP) change.",
        verbose_name="Last ISP Change"
    )
    is_deleted = models.BooleanField(
        blank=False,
        default=0,
        null=False,
        help_text="Is the player character deleted?",
        verbose_name="Is Deleted?"
    )
    deaths = models.PositiveSmallIntegerField(
        help_text="Number of times that the player has died.",
        verbose_name="Deaths"
    )
    total_renown = models.PositiveSmallIntegerField(
        help_text="Total amount of renown earned by the player.",
        verbose_name="Total Renown"
    )
    quests_completed = models.PositiveSmallIntegerField(
        help_text="Total number of quests completed by the player.",
        verbose_name="Quests Completed"
    )
    challenges_completed = models.PositiveSmallIntegerField(
        help_text="Total number of challenges completed by the player.",
        verbose_name="Challenges Completed"
    )
    game_type = models.IntegerField(
        help_text="Player game type.",
        verbose_name="Game Type",
        choices=settings.GAME_TYPES
    )
    birth = models.DateTimeField(
        help_text="Date and time that the player was created.",
        verbose_name="Birth"
    )
    logon = models.DateTimeField(
        help_text="Date and time that the player last logged on.",
        verbose_name="Log On"
    )
    logout = models.DateTimeField(
        help_text="Date and time that the player last logged out.",
        verbose_name="Log Out"
    )

    class Meta:
        managed = False
        db_table = "players"
        default_related_name = "player"
        ordering = ("-true_level", "id")
        verbose_name = "Player"

    def __repr__(self) -> str:
        return (
            f"Player: {repr(self.__str__())} ({self.id}) [{self.player_type}]'"
        )

    def __str__(self) -> str:
        return self.name

    @property
    @admin.display(description="Create IP", ordering="create_haddr")
    def _create_haddr(self):
        """
        IP address that created the account.
        """
        return dec2ip(self.create_haddr)

    @property
    @admin.display(description="Login Fail IP", ordering="login_fail_haddr")
    def _login_fail_haddr(self):
        """
        Last IP address that failed to log in to the account.
        """
        return dec2ip(self.login_fail_haddr)

    @property
    @admin.display(description="Last IP", ordering="last_haddr")
    def _last_haddr(self):
        """
        Last IP address that logged in to the account.
        """
        return dec2ip(self.last_haddr)

    @admin.display(boolean=True, description="Consort?", ordering="-true_level")
    def is_consort(self) -> bool:
        """
        Boolean whether player is consort, or above.
        """
        return self.is_immortal_type(immortal_type="Consort")

    @admin.display(boolean=True, description="Eternal?", ordering="-true_level")
    def is_eternal(self) -> bool:
        """
        Boolean whether player is eternal, or above.
        """
        return self.is_immortal_type(immortal_type="Eternal")

    @admin.display(boolean=True, description="Forger?", ordering="-true_level")
    def is_forger(self) -> bool:
        """
        Boolean whether player is consort, or above.
        """
        return self.is_immortal_type(immortal_type="Forger")

    @admin.display(boolean=True, description="God?", ordering="-true_level")
    def is_god(self) -> bool:
        """
        Boolean whether player is a "God".
        """
        return self.is_immortal_type(immortal_type="God")

    @admin.display(boolean=True, description="Immortal?", ordering="-true_level")
    def is_immortal(self) -> bool:
        """
        Boolean whether player is immortal, or above, but not consort.
        """
        return self.is_immortal_type(immortal_type="Immortal")

    def is_immortal_type(self, immortal_type="Immortal") -> bool:
        """
        Boolean whether player is an immortal of a certain type, or above.
        """
        if self.true_level >= get_immortal_level(immortal_type=immortal_type):
            return True
        return False

    @admin.display(boolean=True, description="Survival?", ordering='-game_type')
    def is_survival(self) -> bool:
        """
        Boolean whether player is Survival ("perm-death").
        """
        if self.game_type == 1:
            return True
        return False

    @admin.display(boolean=False, description="Level", ordering='true_level')
    def level(self) -> int:
        return self.true_level

    @property
    def player_stats(self) -> dict:
        """
        Player stats.
        """

        # Start with empty dictionary.
        stats = {}

        # Immortals have no stats.
        if self.is_immortal() is True:
            return stats

        # No stats for mortal players below level five (5),
        #   with less than one (1) hour of play-time
        if self.true_level < 5 and self.online < 3600:
            return stats

        # TODO: PlayerCommon

        # Otherwise, get the players actual stats
        players_stats = {
            'Agility': self.common.agility,
            'Endurance': self.common.endurance,
            'Focus': self.common.focus,
            'Perception': self.common.perception,
            'Strength': self.common.strength,
            'Willpower': self.common.willpower
        }

        # Put the players stats in the appropriate order,
        #   based on their class, and return them
        for stat_order in self.common.player_class.stats_order:
            stats[stat_order] = players_stats[stat_order]
        return stats

    def get_immortal_type(self) -> (str, None):
        """
        Type of immortal.
        Returns one of settings.IMMORTAL_LEVELS tuple text values,
            from settings.IMMORTAL_LEVELS, or None.
        """
        return get_immortal_type(level=self.true_level)

    def get_player_phrase(self) -> str:
        """
        Player phrase.
        """
        if self.is_deleted is True:
            return "was"
        return "is"

    def get_player_phrase_own(self) -> str:
        """
        Player phrase for ownership.
        """
        if self.is_deleted is True:
            return "were"
        return "are"

    def get_player_phrase_owns(self) -> str:
        """
        Player phrase for plural ownership.
        """
        if self.is_deleted is True:
            return "had"
        return "has"

    def get_player_gender(self) -> str:
            """
            Player gender.
            """
            if self.common.sex == 1:
                return "he"

            if self.common.sex == 2:
                return "she"

            return "they"

    def get_player_gender_own(self) -> str:
        """
        Player gender ownership.
        """
        if self.sex == 1:
            return "his"

        if self.sex == 2:
            return "her"

        return "their"

    def get_player_gender_owns(self) -> str:
        """
        Player gender ownership plural.
        """
        if self.sex == 1:
            return "his"

        if self.sex == 2:
            return "hers"

        return "have"

    def get_player_type(self):
        """
        Get the type pf player (string), returns one of:
            - Dead
            - An immortal type:
                * One of settings.IMMORTAL_LEVELS tuple text values.
            - Survival
            - Classic
        """
        if self.is_deleted == 1:
            return "Dead"

        if self.true_level >= min(settings.IMMORTAL_LEVELS)[0]:
            return get_immortal_type(level=self.true_level)

        if self.is_survival() is True:
            return "Survival"

        return "Classic"

    @admin.display(boolean=False, description="Type")
    def player_type(self) -> str:
        """
        Player type.
        """
        return self.get_player_type()

    @property
    def podir(self) -> str:
        """
        Player "Podir" folder on disk.
        """
        return f'{settings.MUD_PODIR}/{self.name}'

    @property
    @admin.display(description="Seasonal Earned", ordering="seasonal_earned")
    def seasonal_earned(self) -> int:
        """
        Amount of essence earned for the player.
        """

        # Immortal players do not earn essence
        if self.is_immortal() is True:
            return 0

        # Survival players earn less essence from renown
        divisor = 10
        if self.is_survival() is True:
            divisor = 20

        # Start with two (2) points for existing,
        #   with renown/remort equation
        earned = int(self.total_renown / divisor) + 2
        if self.remorts > 0:
            earned += int(self.remorts / 5) * 3 + 1
        return earned


class RemortUpgrade(models.Model):
    """
    Remort Upgrade.
    """
    upgrade_id = models.PositiveIntegerField(
        help_text=(
            "Auto-generated, permanent identification number of the "
            "remort upgrade."
        ),
        primary_key=True,
        verbose_name="Upgrade ID"
    )
    name = models.CharField(
        help_text="Name of the remort upgrade.",
        max_length=20,
        unique=True,
        verbose_name="Name"
    )
    renown_cost = models.PositiveSmallIntegerField(
        help_text="Renown cost of the remort upgrade.",
        verbose_name="Renown Cost"
    )
    max_value = models.PositiveSmallIntegerField(
        help_text="Maximum value of the remort upgrade.",
        verbose_name="Maximum Value"
    )
    scale = models.IntegerField(
        help_text="Scale of the remort upgrade.",
        verbose_name="Scale"
    )
    display_name = models.CharField(
        help_text="Display name of the remort upgrade.",
        max_length=30,
        verbose_name="Display Name"
    )
    can_buy = models.BooleanField(
        help_text="Whether the remort upgrade can be bought.",
        verbose_name="Can Buy?"
    )
    bonus = models.IntegerField(
        help_text="Bonus of the remort upgrade.",
        verbose_name="Bonus"
    )
    survival_scale = models.IntegerField(
        help_text="Scale of the remort upgrade, for survival players.",
        verbose_name="Survival Scale"
    )
    survival_renown_cost = models.IntegerField(
        help_text="Renown cost of the remort upgrade, for survival players.",
        verbose_name="Survival Renown Cost"
    )

    class Meta:
        db_table = "remort_upgrades"
        managed = False
        ordering = ("-can_buy", "display_name",)
        verbose_name = "Remort Upgrade"

    def __repr__(self):
        return f"{self.__class__.__name__}: {repr(self.__str__())}"

    def __str__(self):
        return self.display_name
