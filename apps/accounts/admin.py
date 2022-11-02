from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _

from . forms import CustomAdminUserChangeForm, CustomAdminUserCreationForm
from . models import BlockedContact, Timezone, User

class Group(DjangoGroup):
    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
        proxy = True

class GroupAdmin(BaseGroupAdmin):
    pass


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomAdminUserCreationForm
    form = CustomAdminUserChangeForm
    model = User

    list_display = [
        "pkid",
        "id",
        "email",
        "name",
        "phone",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "name",
        "phone",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "phone", "password")},
        ),
        (
            _("Personal Information"),
            {"fields": ("name", "tz", "status", "avatar")},
        ),
        (
            _("Page Look"),
            {"fields": ("theme", "wallpaper")},
        ),
        (
            _("Privacy Settings"),
            {"fields": ("last_seen", "avatar_status", "about_status", "group_status", "message_timer", "read_receipts", "blocked_contacts")},
        ),
        (
            _("Notification Settings"),
            {"fields": ("message_notifications", "show_previews", "show_reaction_notifications", "sounds", "security_notifications")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {"fields": ("date_joined", "last_login")},
        ),
    )

    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "phone", "tz", "password1", "password2", "is_staff", "is_active"),
            }
        ),
    )

    search_fields = ["email", "name", "phone"]

    def render_change_form(self, request, context, obj, add=False, change=False, form_url=''):
        if not '/add/' in request.path:
            # Allow only super users and article owner to update article
            if request.user != obj and request.user.is_superuser != True:
                context.update({
                    'show_save': False,
                    'show_save_and_continue': False,
                    'show_delete': False,
                    'show_save_and_add_another': False
                })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_readonly_fields(self, request, obj=None):
       if not request.user.is_superuser:
           self.readonly_fields = ['groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active']
       return self.readonly_fields

class BlockedContactAdmin(admin.ModelAdmin):
    list_display = ["blocker", "blockee", "created_at"]
    list_filter = ["blocker", "blockee", "created_at"]

class TimezoneAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    list_filter = ["name", "created_at"]


admin.site.register(User, UserAdmin)
admin.site.register(BlockedContact, BlockedContactAdmin)
admin.site.register(Timezone, TimezoneAdmin)

admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)