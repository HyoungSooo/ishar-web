from django.contrib import admin

from ishar.apps.faqs.models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Ishar news administration.
    """
    date_hierarchy = "created"
    fieldsets = (
        (None, {"fields": ("faq_id", "slug")}),
        ("Question", {"fields": ("question_text", "question_answer")}),
        ("Authorship", {"fields": ("created", "account")}),
        ("Display", {"fields": ("is_visible", "display_order")}),
    )
    list_display = (
        "faq_id", "slug", "question_text", "is_visible", "display_order"
    )
    list_display_links = ("faq_id", "slug", "question_text")
    list_filter = ("is_visible", ("account", admin.RelatedOnlyFieldListFilter))
    readonly_fields = ("faq_id", "account", "created")
    search_fields = (
        "slug", "question_text", "question_answer", "account", "is_visible"
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.account = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_god():
                return True
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            if request.user.is_god():
                return True
        return False

    def has_module_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if request.user and not request.user.is_anonymous:
            return request.user.is_god()
        return False
