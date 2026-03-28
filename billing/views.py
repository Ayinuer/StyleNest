from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def billing_page(request):
    return render(request, 'billing/billing.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })


@login_required
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': 'StyleNest Monthly Subscription',
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/billing/success/',
        cancel_url='http://127.0.0.1:8000/billing/cancel/',
    )
    return JsonResponse({'id': session.id})