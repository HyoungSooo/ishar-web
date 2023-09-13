from django.contrib import admin

from ..models.prereq import QuestPrereq


@admin.register(QuestPrereq)
class QuestPrereqsAdmin(admin.ModelAdmin):
    """
    Ishar quest prerequisite administration.
    """
    fieldsets = (
        (None, {"fields": ("quest", "required_quest")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = search_fields = ("quest", "required_quest")
    list_filter = (("quest", admin.RelatedOnlyFieldListFilter),)
    model = QuestPrereq


class QuestPrereqsAdminInline(admin.TabularInline):
    """
    Ishar quest prerequisite administration inline.
    """
    fk_name = "quest"
    model = QuestPrereq
