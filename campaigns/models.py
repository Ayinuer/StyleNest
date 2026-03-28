from django.db import models
from django.utils import timezone
from accounts.models import ShopOwnerProfile


class Campaign(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    ]

    TEMPLATE_CHOICES = [
        ('custom', 'Custom'),
        ('new_arrivals', 'New Arrivals'),
        ('sale_alert', 'Sale Alert'),
        ('birthday_offer', 'Birthday Offer'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
    ]

    shop = models.ForeignKey(
        ShopOwnerProfile,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    title = models.CharField(max_length=200)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='custom')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='sms')
    message_body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_for = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    total_recipients = models.PositiveIntegerField(default=0)
    delivered_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title