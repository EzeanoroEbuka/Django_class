from django.contrib import admin

from user.models import Customer
from  django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(Customer)
class UserAdmin(BaseUserAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "first_name", "last_name", "email"),
            },
        ),
    )
