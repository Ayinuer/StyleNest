from celery import shared_task
from django.utils import timezone
from store.models import Subscriber
from .models import Campaign


@shared_task
def send_scheduled_campaigns():
    now = timezone.now()

    campaigns = Campaign.objects.filter(
        status='scheduled',
        scheduled_for__lte=now
    )

    for campaign in campaigns:
        subscribers = Subscriber.objects.filter(
            shop=campaign.shop,
            is_active=True
        )

        total_recipients = subscribers.count()

        delivered = 0
        failed = 0

        for subscriber in subscribers:
            try:
                # Simulated delivery
                # Replace later with Twilio or WhatsApp API
                print(
                    f"[{campaign.message_type.upper()}] "
                    f"To: {subscriber.phone_number} | "
                    f"Message: {campaign.message_body}"
                )
                delivered += 1
            except Exception:
                failed += 1

        campaign.status = 'sent'
        campaign.sent_at = now
        campaign.total_recipients = total_recipients
        campaign.delivered_count = delivered
        campaign.failed_count = failed
        campaign.save()