from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShopOwnerProfile


# ✅ CREATE profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopOwnerProfile.objects.create(
            user=instance,
            shop_name=instance.username
        )


# ✅ SAVE profile when user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'shopownerprofile'):
        instance.shopownerprofile.save()