from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    encrypted_password = models.BinaryField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_name} ({self.login})"

class PasswordShareLink(models.Model):
    password_entry = models.ForeignKey(PasswordEntry, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)  # pour usage unique

    def is_valid(self):
        return timezone.now() < self.expires_at and not self.used