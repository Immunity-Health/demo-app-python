from django.conf import settings
from django.db import models


class Permission(models.Model):
    code = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserPermission",
        related_name="direct_permissions",
        blank=True,
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, default="")
    permissions = models.ManyToManyField(
        Permission, through="RolePermission", related_name="roles", blank=True
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="UserRole", related_name="rbac_roles", blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role} -> {self.permission}"


class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user} -> {self.role}"


class UserPermission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = ("user", "permission")

    def __str__(self):
        return f"{self.user} -> {self.permission}"
