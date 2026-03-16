from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ("fullName", "email", "phone", "avatar")


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "fullname_from_profile",
        "email_from_profile",
        "phone_from_profile",
        "is_staff",
    )

    def fullname_from_profile(self, obj):
        return obj.profile.fullName if hasattr(obj, "profile") else "-"

    fullname_from_profile.short_description = "Полное имя"

    def email_from_profile(self, obj):
        return obj.profile.email if hasattr(obj, "profile") else "-"

    email_from_profile.short_description = "Email"

    def phone_from_profile(self, obj):
        return obj.profile.phone if hasattr(obj, "profile") else "-"

    phone_from_profile.short_description = "Телефон"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
