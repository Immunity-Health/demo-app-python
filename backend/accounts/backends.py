from django.db.models import Q

from .models import Permission


class RBACBackend:
    """Permission-only backend: resolves has_perm()/get_all_permissions() against
    the custom Role/Permission tables. Does not authenticate users itself."""

    def authenticate(self, request, **kwargs):
        return None

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj or not user_obj.is_active:
            return set()
        if user_obj.is_superuser:
            return set(Permission.objects.values_list("code", flat=True))
        codes = Permission.objects.filter(
            Q(users=user_obj) | Q(roles__users=user_obj)
        ).values_list("code", flat=True)
        return set(codes)

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj=obj)

    def has_module_perms(self, user_obj, app_label):
        return any(
            code.startswith(f"{app_label}.") for code in self.get_all_permissions(user_obj)
        )
