from django.db import models
from shops.models import ShopOwner
from cryptography.fernet import Fernet
from django.conf import settings


class Subscriber(models.Model):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    shop = models.ForeignKey(
        ShopOwner,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    encrypted_phone_number = models.TextField()
    birth_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_phone_number(self, raw_phone_number):
        fernet = Fernet(settings.FERNET_KEY.encode())
        self.encrypted_phone_number = fernet.encrypt(
            raw_phone_number.encode()
        ).decode()

    def get_phone_number(self):
        fernet = Fernet(settings.FERNET_KEY.encode())
        return fernet.decrypt(
            self.encrypted_phone_number.encode()
        ).decode()

    def matches_phone_number(self, raw_phone_number):
        try:
            return self.get_phone_number() == raw_phone_number
        except Exception:
            return False

    def __str__(self):
        return f"Subscriber for {self.shop.shop_name} - {self.birth_month}"