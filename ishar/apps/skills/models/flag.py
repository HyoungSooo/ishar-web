from django.db import models


class SpellFlag(models.Model):
    """
    Spell Flag.
    """
    id = models.AutoField(
        blank=False,
        editable=False,
        help_text=(
            "Auto-generated permanent identification number for a spell flag."
        ),
        null=False,
        primary_key=True,
        verbose_name="Spell Flag ID"
    )
    name = models.CharField(
        max_length=50,
        help_text="Name of the spell flag.",
        verbose_name="Spell Flag Name"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Description of the spell flag.",
        verbose_name="Spell Flag Description"
    )

    class Meta:
        db_table = "spell_flags"
        managed = False
        ordering = ("name",)
        verbose_name = "Flag"

    def __repr__(self):
        return f"{self.__class__.__name__} : {repr(self.__str__())} ({self.id})"

    def __str__(self):
        return self.name
