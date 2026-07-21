from django.db import models

from .encryption import decrypt_value, encrypt_value


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_encrypted = models.TextField(blank=True, default="")
    address_encrypted = models.TextField(blank=True, default="")
    aadhar_number_encrypted = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def phone(self) -> str:
        if not self.phone_encrypted:
            return ""
        return decrypt_value(self.phone_encrypted)

    @phone.setter
    def phone(self, value: str) -> None:
        self.phone_encrypted = encrypt_value(value)

    @property
    def address(self) -> str:
        if not self.address_encrypted:
            return ""
        return decrypt_value(self.address_encrypted)

    @address.setter
    def address(self, value: str) -> None:
        self.address_encrypted = encrypt_value(value)

    @property
    def aadhar_number(self) -> str:
        if not self.aadhar_number_encrypted:
            return ""
        return decrypt_value(self.aadhar_number_encrypted)

    @aadhar_number.setter
    def aadhar_number(self, value: str) -> None:
        self.aadhar_number_encrypted = encrypt_value(value)
