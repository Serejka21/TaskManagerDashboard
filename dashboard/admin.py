from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dashboard.models import Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("first_name", "last_name", "position",)}),)
    )
