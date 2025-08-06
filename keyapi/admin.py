from django.contrib import admin
from .models import Key
from rest_framework.authtoken.models import Token
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
import secrets
from binascii import hexlify

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'salt', 'last_updated', 'regenerate_key', 'copy_token']

    def regenerate_key(self, obj):
        return format_html(
            '<a class="button" href="regenerate/{}/">Regenerate</a>',
            obj.id
        )
    regenerate_key.short_description = 'Regenerate Key'
    regenerate_key.allow_tags = True

    def copy_token(self, obj):
        token = Token.objects.get(user=obj.user)
        return format_html(
            '<input type="text" value="{}" style="width: 300px;" readonly onclick="this.select();document.execCommand(\'copy\');" />',
            token.key
        )
    copy_token.short_description = 'Copy API Token'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('regenerate/<int:key_id>/', self.admin_site.admin_view(self.regenerate)),
        ]
        return custom_urls + urls

    def regenerate(self, request, key_id):
        key_obj = Key.objects.get(pk=key_id)
        key_obj.key = hexlify(secrets.token_bytes(32)).decode()
        key_obj.salt = hexlify(secrets.token_bytes(8)).decode()[:16]
        key_obj.save()
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))
