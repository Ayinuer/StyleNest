from django.db import models
from django.contrib.auth.models import User
import secrets


def generate_qr_token():
    return secrets.token_urlsafe(16)


class ShopOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    shop_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)

    # 🔥 unique QR link identifier
    qr_token = models.CharField(
        max_length=100,
        unique=True,
        default=generate_qr_token,
        editable=False
    )

    # 🔥 Stripe integration (future use)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)

    # 🔥 subscription status
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_subscribe_url(self):
        return f"/subscribe/{self.qr_token}/"

    def __str__(self):
        return self.shop_name
# Create your models here.
