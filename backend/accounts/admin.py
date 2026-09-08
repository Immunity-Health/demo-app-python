from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Permission, Role, RolePermission, UserPermission, UserRole

User = get_user_model()


class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1


class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1


class UserPermissionInline(admin.TabularInline):
    model = UserPermission
    extra = 1


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [RolePermissionInline]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code",)


admin.site.unregister(User)


@admin.register(User)
class RBACUserAdmin(UserAdmin):
    inlines = [*UserAdmin.inlines, UserRoleInline, UserPermissionInline]
