from django.contrib import admin

from .models import Patch


@admin.register(Patch)
class PatchAdmin(admin.ModelAdmin):
    """
    Ishar patch administration.
    """
    date_hierarchy = "patch_date"
    fieldsets = (
        (None, {"fields": ("patch_id", "is_visible")}),
        ("Content", {"fields": ("patch_name", "patch_file")}),
        ("Authorship", {"fields": ("patch_date", "account")}),
    )
    filter_horizontal = filter_vertical = ()
    list_display = (
        "patch_name", "patch_file", "patch_date", "is_visible", "account"
    )
    list_filter = ("is_visible", ("account", admin.RelatedOnlyFieldListFilter))
    readonly_fields = ("patch_id", "account")
    search_fields = ("patch_name", "account", "patch_date", "is_visible")

    def save_model(self, request, obj, form, change):
        """
        For newly added patches, the account is the uploading user.
        """
        if not change:
            obj.account = request.user
        super().save_model(request, obj, form, change)
