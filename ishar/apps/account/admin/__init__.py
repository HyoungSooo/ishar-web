from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .upgrade import AccountUpgradeAdmin


@admin.register(get_user_model())
class AccountAdmin(BaseUserAdmin):
    """
    Ishar account administration.
    """

    def has_add_permission(self, request, obj=None):
        """
        Disabling adding accounts in /admin/.
        """
        return False

    model = get_user_model()

    fieldsets = (
        (
            None, {
                "fields": (
                    "account_id", model.USERNAME_FIELD, model.EMAIL_FIELD
                )
            }
        ),
        (
            "Points", {
                "fields": (
                    "current_essence", "earned_essence", "bugs_reported"
                )
            }
        ),
        (
            "Last", {
                "fields": ("last_ident", "last_isp", "_last_haddr")
            }
        ),
        (
            "Created", {
                "classes": ("collapse",),
                "fields": ("create_ident", "create_isp", "_create_haddr")
            }
        ),
        (
            "Dates", {
                "classes": ("collapse",),
                "fields": ("account_gift", "banned_until", "created_at")
            }
        )
    )
    excludes = filter_horizontal = filter_vertical = inlines = list_filter = ()
    list_display = (
        model.USERNAME_FIELD, "player_count", "is_god", "is_immortal",
        "current_essence"
    )
    ordering = ("account_id",)
    search_fields = (
        model.USERNAME_FIELD, model.EMAIL_FIELD,
        "create_isp", "create_ident", "last_ident", "last_isp",
        "_create_haddr", "_login_fail_haddr", "_last_haddr"
    )
    readonly_fields = (
        "account_id", "last_ident", "last_isp", "_last_haddr",
        "created_at", "create_isp", "create_ident", "_create_haddr",
        "player_count"
    )
