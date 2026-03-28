from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def billing_page(request):
    return render(request, 'billing/billing.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })