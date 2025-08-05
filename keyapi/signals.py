import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Key
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_user_key(sender, instance, created, **kwargs):
    if created:
        from secrets import token_bytes
        from binascii import hexlify

        aes_key = hexlify(token_bytes(32)).decode()  # 256-bit key
        salt = hexlify(token_bytes(8)).decode()[:16]
        Key.objects.create(user=instance, key=aes_key, salt=salt)
        Token.objects.create(user=instance)
