from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import AdvancedUser


class AdvancedUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "is_active",
        "is_staff",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(AdvancedUser, AdvancedUserAdmin)
