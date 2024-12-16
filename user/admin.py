from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import User, Pupil, Teacher, Parent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'full_name']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("full_name", "image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("full_name", "image", "username", "password1", "password2"),
            },
        ),
    )


admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Pupil)
