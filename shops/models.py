from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)

    # ✅ ADD THESE TWO
    slug = models.SlugField(unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.shop_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name