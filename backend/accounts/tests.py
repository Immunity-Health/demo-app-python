from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Permission, Role

User = get_user_model()


class RBACBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ada@example.com", email="ada@example.com")
        self.view_perm = Permission.objects.get(code="customers.view_customer")
        self.add_perm = Permission.objects.get(code="customers.add_customer")

    def test_user_with_no_grants_has_no_permission(self):
        self.assertFalse(self.user.has_perm("customers.view_customer"))

    def test_role_grants_permission(self):
        role = Role.objects.get(name="Viewer")
        role.users.add(self.user)
        self.assertTrue(self.user.has_perm("customers.view_customer"))
        self.assertFalse(self.user.has_perm("customers.add_customer"))

    def test_direct_permission_grant(self):
        self.add_perm.users.add(self.user)
        self.assertTrue(self.user.has_perm("customers.add_customer"))
        self.assertFalse(self.user.has_perm("customers.view_customer"))


class CustomerApiPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="grace@example.com", email="grace@example.com")

    def test_anonymous_get_is_unauthorized(self):
        response = self.client.get(reverse("customer_api"))
        self.assertEqual(response.status_code, 401)

    def test_authenticated_without_permission_is_forbidden(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("customer_api"))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_with_permission_succeeds(self):
        Permission.objects.get(code="customers.view_customer").users.add(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse("customer_api"))
        self.assertEqual(response.status_code, 200)
