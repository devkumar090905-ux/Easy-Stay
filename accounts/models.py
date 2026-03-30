from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Valid for 10 minutes
        return timezone.now() < self.created_at + datetime.timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"
