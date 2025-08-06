import binascii
from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
import os

class Key(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
    salt = models.CharField(max_length=32)
    last_updated = models.DateTimeField(auto_now=True)

    def refresh_if_needed(self):
        if timezone.now() - self.last_updated > timedelta(weeks=1):
            self.key = binascii.hexlify(os.urandom(32)).decode()  # 256-bit key
            self.salt = binascii.hexlify(os.urandom(16)).decode()  # 128-bit salt
            self.save()

    def __str__(self):
        return f"{self.user.username}'s Key"
