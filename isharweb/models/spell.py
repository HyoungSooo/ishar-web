from django.db import models
from django.contrib import admin

from .force import Force


class SpellFlag(models.Model):
    """
    Spell Flag.
    """
    id = models.IntegerField(
        primary_key=True,
        help_text=(
            "Auto-generated permanent identification number for a spell flag."
        ),
        verbose_name="Spell Flag ID"
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the spell flag.",
        verbose_name="Spell Flag Name"
    )
    description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Description of the spell flag.",
        verbose_name="Spell Flag Description"
    )

    class Meta:
        managed = False
        db_table = "spell_flags"
        ordering = ("name",)
        verbose_name = "Spell Flag"
        verbose_name_plural = "Spell Flags"

    def __repr__(self):
        return f"Spell Flag: {repr(self.__str__())} ({self.id})"

    def __str__(self):
        return self.name


class Spell(models.Model):
    """
    Spell.
    """
    enum_symbol = models.CharField(
        max_length=255,
        help_text="Internal ENUM symbol of the skill.",
        verbose_name="ENUM Symbol"
    )
    func_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Internal function name for the skill.",
        verbose_name="Function Name"
    )
    skill_name = models.TextField(
        blank=True, null=True,
        help_text="Friendly name of the skill.",
        verbose_name="Skill Name"
    )
    min_posn = models.IntegerField(
        blank=True, null=True,
        help_text="Minimum posn.",
        verbose_name="Minimum posn"
    )
    min_use = models.IntegerField(
        blank=True, null=True,
        help_text="Minimum use.",
        verbose_name="Minimum use"
    )
    spell_breakpoint = models.IntegerField(
        blank=True, null=True,
        help_text="Breakpoint of the spell",
        verbose_name="Spell Breakpoint"
    )
    held_cost = models.IntegerField(
        blank=True, null=True,
        help_text="Held cost of the skill",
        verbose_name="Held Cost"
    )
    wearoff_msg = models.TextField(
        blank=True, null=True,
        help_text="Wear-off message shown to the user when the skill fades.",
        verbose_name="Wear-Off Message"
    )
    chant_text = models.TextField(
        blank=True, null=True,
        help_text="Text chanted to implement the skill.",
        verbose_name="Chant Text"
    )
    difficulty = models.IntegerField(
        blank=True, null=True,
        help_text="Difficulty of the skill.",
        verbose_name="Difficulty"
    )
    rate = models.IntegerField(
        blank=True, null=True,
        help_text="Rate of the skill.",
        verbose_name="Rate"
    )
    notice_chance = models.IntegerField(
        blank=True, null=True,
        help_text="Scale.",
        verbose_name="Scale"
    )
    appearance = models.TextField(
        blank=True, null=True,
        help_text="Appearance.",
        verbose_name="Appearance"
    )
    component_type = models.IntegerField(
        blank=True, null=True,
        help_text="Component type.",
        verbose_name="Component Type"
    )
    component_value = models.IntegerField(
        blank=True, null=True,
        help_text="Component value.",
        verbose_name="Component Value"
    )
    scale = models.IntegerField(
        blank=True, null=True,
        help_text="Scale.",
        verbose_name="Scale"
    )
    mod_stat_1 = models.IntegerField(
        blank=True, null=True,
        help_text="Mod stat 1.",
        verbose_name="Mod Stat 1"
    )
    mod_stat_2 = models.IntegerField(
        blank=True, null=True,
        help_text="Mod stat 1.",
        verbose_name="Mod Stat 1"
    )
    is_spell = models.IntegerField(
        blank=True, null=True,
        choices=[(0, False), (1, True)],
        help_text="Is this a spell?",
        verbose_name="Is Spell?"
    )
    is_skill = models.IntegerField(
        blank=True, null=True,
        choices = [(0, False), (1, True)],
        help_text="Is this a skill?",
        verbose_name="Is Skill?"
    )
    is_type = models.IntegerField(
        blank=True, null=True,
        choices=[(0, False), (1, True)],
        help_text="Is this a type?",
        verbose_name="Is Type?"
    )
    decide_func = models.TextField(
        blank=True, null=True,
        help_text="Internal function for decision-making.",
        verbose_name="Decide Function"
    )

    class Meta:
        managed = False
        db_table = "spell_info"
        ordering = (
            "-is_spell", "-is_skill", "-is_type", "skill_name", "enum_symbol"
        )
        verbose_name = "Spell"
        verbose_name_plural = "Spells"

    def __repr__(self):
        return f"Spell: {repr(self.__str__())}"

    def __str__(self):
        return self.skill_name or self.enum_symbol

    @admin.display(boolean=True, description="Skill?", ordering="is_skill")
    def _is_skill(self):
        """
        Boolean whether a skill.
        """
        if self.is_skill == 1:
            return True
        return False

    @admin.display(boolean=True, description="Spell?", ordering="is_spell")
    def _is_spell(self):
        """
        Boolean whether a spell.
        """
        if self.is_spell == 1:
            return True
        return False

    @admin.display(boolean=True, description="Type?", ordering="is_type")
    def _is_type(self):
        """
        Boolean whether a type.
        """
        if self.is_type == 1:
            return True
        return False


class SpellForce(models.Model):
    spell = models.OneToOneField(
        to=Spell,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        help_text="Spell related to a force.",
        verbose_name="Spell"
    )
    force = models.ForeignKey(
        to=Force,
        on_delete=models.DO_NOTHING,
        help_text="Force related to the spell.",
        verbose_name="Force"
    )

    class Meta:
        managed = False
        db_table = "spell_forces"
        ordering = ("spell", "force")
        verbose_name = "Spell Force"
        verbose_name_plural = "Spell Forces"

    def __repr__(self):
        return f"Spell Force: {self.spell} @ {self.force}"

    def __str__(self):
        return self.__repr__()


class SpellSpellFlag(models.Model):
    """
    Spell association to a spell flag.
    """
    spell = models.OneToOneField(
        to=Spell,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        help_text="Spell affected by the flag.",
        verbose_name="Spell"
    )
    flag = models.ForeignKey(
        to=SpellFlag,
        on_delete=models.DO_NOTHING,
        help_text="Flag affecting the spell.",
        verbose_name="Flag"
    )

    # The composite primary key (spell_id, flag_id) found,
    #   that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = "spells_spell_flags"
        ordering = ("spell", "flag")
        unique_together = (("spell", "flag"),)
        verbose_name = "Spell's Flag"
        verbose_name_plural = "Spell's Flags"

    def __repr__(self):
        return f"Spell's Flag: {self.spell} @ {self.flag}"

    def __str__(self):
        return self.__repr__()
