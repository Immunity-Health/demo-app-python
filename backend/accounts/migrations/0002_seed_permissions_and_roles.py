from django.db import migrations

PERMISSIONS = [
    ("customers.view_customer", "Can view customers"),
    ("customers.add_customer", "Can add customers"),
    ("customers.delete_customer", "Can delete customers"),
]

ROLES = {
    "Admin": ["customers.view_customer", "customers.add_customer", "customers.delete_customer"],
    "Viewer": ["customers.view_customer"],
}


def seed(apps, schema_editor):
    Permission = apps.get_model("accounts", "Permission")
    Role = apps.get_model("accounts", "Role")
    RolePermission = apps.get_model("accounts", "RolePermission")

    codes_to_permission = {}
    for code, description in PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            code=code, defaults={"description": description}
        )
        codes_to_permission[code] = permission

    for role_name, codes in ROLES.items():
        role, _ = Role.objects.get_or_create(name=role_name)
        for code in codes:
            RolePermission.objects.get_or_create(
                role=role, permission=codes_to_permission[code]
            )


def unseed(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    Permission = apps.get_model("accounts", "Permission")
    Role.objects.filter(name__in=ROLES.keys()).delete()
    Permission.objects.filter(code__in=[code for code, _ in PERMISSIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
