from django.contrib import admin

from ..models.reward import QuestReward


@admin.register(QuestReward)
class QuestRewardsAdmin(admin.ModelAdmin):
    """
    Ishar quest reward administration.
    """
    fieldsets = (
        (None, {"fields": ("quest_reward_id",)}),
        ("Type", {"fields": ("reward_type",)}),
        ("Number", {"fields": ("reward_num",)}),
        ("Quest", {"fields": ("quest",)}),
        ("Class", {"fields": ("class_restrict",)})
    )
    list_display = ("quest_reward_id", "reward_type", "quest", "class_restrict")
    list_filter = (
        "reward_type", "class_restrict",
        ("quest", admin.RelatedOnlyFieldListFilter)
    )
    model = QuestReward
    readonly_fields = ("quest_reward_id",)
    search_fields = ("reward_num", "reward_type", "quest", "class_restrict")

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()


class QuestRewardsAdminInline(admin.TabularInline):
    """
    Ishar quest reward administration inline.
    """
    extra = 1
    model = QuestReward

    def has_module_permission(self, request, obj=None):
        return request.user.is_immortal()
