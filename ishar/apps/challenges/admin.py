from django.contrib import admin

from .models import Challenge


class ChallengeCompletedListFilter(admin.SimpleListFilter):
    title = "Completed"
    parameter_name = "is_completed"

    def lookups(self, request, model_admin):
        return (
            (1, "Yes"),
            (0, "No")
        )

    def queryset(self, request, queryset):
        """
        Determine whether a challenge is complete based on whether
            the "winner_desc" column is empty or not.
        """
        qs = queryset
        if self.value():
            if self.value() == "1":
                qs = qs.exclude(winner_desc="")
            if self.value() == "0":
                qs = qs.filter(winner_desc="")
        return qs


@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    """
    Ishar challenge administration.
    """
    fieldsets = (
        (None, {"fields": ("challenge_id", "is_active")}),
        ("Details", {"fields": ("challenge_desc", "winner_desc")}),
        ("Target", {"fields": ("mob_vnum", "mob_name")}),
        ("Original", {"fields": ("orig_level", "orig_people", "orig_tier")}),
        ("Adjusted", {"fields": ("adj_level", "adj_people", "adj_tier")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = ("challenge_desc", "is_active", "is_completed")
    list_filter = ("is_active", ChallengeCompletedListFilter)
    readonly_fields = ("challenge_id",)
    search_fields = ("challenge_desc", "winner_desc", "mob_vnum", "mob_name")

    def has_add_permission(self, request, obj=None):
        return request.user.is_god()

    def has_change_permission(self, request, obj=None):
        return request.user.is_god()

    def has_view_permission(self, request, obj=None):
        return request.user.is_eternal()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_god()
