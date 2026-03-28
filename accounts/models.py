from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import secrets
import qrcode
from io import BytesIO
from django.core.files import File


def generate_qr_token():
    return secrets.token_urlsafe(16)


class ShopOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)

    qr_token = models.CharField(
        max_length=100,
        unique=True,
        default=generate_qr_token,
        editable=False
    )
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_subscribe_url(self):
        return reverse('subscribe', kwargs={'qr_token': self.qr_token})

    def get_unsubscribe_url(self):
        return reverse('unsubscribe', kwargs={'qr_token': self.qr_token})

    def get_full_subscribe_url(self):
        return f"{settings.SITE_URL}{self.get_subscribe_url()}"

    def generate_qr_code(self):
        subscribe_url = self.get_full_subscribe_url()

        qr = qrcode.make(subscribe_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        filename = f"{self.user.username}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_token:
            self.qr_token = generate_qr_token()

        super().save(*args, **kwargs)

        if not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return self.shop_name