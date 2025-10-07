# src/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import User
from .resources import UserResource


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    """
    Keep all the BaseUserAdmin conveniences (fieldsets, add_fieldsets, etc.)
    and add CSV Import/Export via django-import-export. Unfold styling is applied
    via the Import/Export forms (no need to inherit Unfold's ModelAdmin here).
    """

    # django-import-export config
    resource_classes = [UserResource]
    import_form_class = ImportForm
    export_form_class = ExportForm

    # your existing config preserved
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role", "is_staff", "is_superuser"),
            },
        ),
    )

    readonly_fields = ("date_joined",)
