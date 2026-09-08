import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Permission

from .encryption import decrypt_value, encrypt_value
from .models import Customer

User = get_user_model()


class EncryptionTests(TestCase):
    def test_encrypt_decrypt_round_trip(self):
        value = "555-1234"
        encrypted = encrypt_value(value)
        self.assertNotEqual(encrypted, value)
        self.assertEqual(decrypt_value(encrypted), value)


class CustomerTests(TestCase):
    def test_customer_pii_is_stored_encrypted(self):
        customer = Customer.objects.create(
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
        )
        customer.phone = "555-1111"
        customer.address = "123 Demo St"
        customer.save()

        customer.refresh_from_db()
        self.assertNotEqual(customer.phone_encrypted, "555-1111")
        self.assertNotEqual(customer.address_encrypted, "123 Demo St")
        self.assertEqual(customer.phone, "555-1111")
        self.assertEqual(customer.address, "123 Demo St")

    def test_customer_api_create_and_list(self):
        user = User.objects.create_user(username="admin@example.com", email="admin@example.com")
        Permission.objects.get(code="customers.view_customer").users.add(user)
        Permission.objects.get(code="customers.add_customer").users.add(user)
        self.client.force_login(user)

        response = self.client.post(
            reverse("customer_api"),
            data=json.dumps(
                {
                    "first_name": "Grace",
                    "last_name": "Hopper",
                    "email": "grace@example.com",
                    "phone": "555-2222",
                    "address": "456 AI Ave",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        list_response = self.client.get(reverse("customer_api"))
        self.assertEqual(list_response.status_code, 200)
        data = list_response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["email"], "grace@example.com")
        self.assertEqual(data[0]["phone"], "555-2222")
