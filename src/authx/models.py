# authx/models.py
import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        USER = "user", "User"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class EmailOTP(models.Model):
    class Purpose(models.TextChoices):
        VERIFY = "verify", "Verify"
        RESET = "reset", "Reset Password"

    user = models.ForeignKey("authx.User", on_delete=models.CASCADE, related_name="email_otps")
    code = models.CharField(max_length=10)
    purpose = models.CharField(max_length=20, choices=Purpose.choices, default=Purpose.VERIFY)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.code} - {self.purpose}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_code(length=6):
        digits = "0123456789"
        return "".join(random.choice(digits) for _ in range(length))