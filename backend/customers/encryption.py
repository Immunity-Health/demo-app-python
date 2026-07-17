import base64
import os
from hashlib import sha256

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings


def _build_key() -> bytes:
    key_value = settings.PII_ENCRYPTION_KEY
    try:
        decoded = base64.urlsafe_b64decode(key_value)
        if len(decoded) == 32:
            return decoded
    except Exception:
        pass
    return sha256(key_value.encode("utf-8")).digest()


def encrypt_value(value: str) -> str:
    if value == "":
        return ""
    aes = AESGCM(_build_key())
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, value.encode("utf-8"), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode("utf-8")


def decrypt_value(value: str) -> str:
    if value == "":
        return ""
    decoded = base64.urlsafe_b64decode(value.encode("utf-8"))
    nonce = decoded[:12]
    ciphertext = decoded[12:]
    aes = AESGCM(_build_key())
    return aes.decrypt(nonce, ciphertext, None).decode("utf-8")
