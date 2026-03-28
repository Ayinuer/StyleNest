from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import ShopOwnerProfile
from .models import Subscriber
from .forms import SubscriberForm, UnsubscribeForm


def subscribe_view(request, qr_token):
    shop = get_object_or_404(ShopOwnerProfile, qr_token=qr_token)

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            raw_phone = form.cleaned_data['phone_number']
            birth_month = form.cleaned_data['birth_month']

            existing_subscribers = Subscriber.objects.filter(shop=shop)

            for subscriber in existing_subscribers:
                if subscriber.matches_phone_number(raw_phone):
                    if subscriber.is_active:
                        messages.info(request, 'You are already subscribed.')
                    else:
                        subscriber.is_active = True
                        subscriber.birth_month = birth_month
                        subscriber.save()
                        messages.success(request, 'Your subscription has been reactivated.')
                    return redirect('subscribe', qr_token=shop.qr_token)

            subscriber = form.save(commit=False)
            subscriber.shop = shop
            subscriber.set_phone_number(raw_phone)
            subscriber.save()

            messages.success(request, 'Subscription successful.')
            return redirect('subscribe_success')
    else:
        form = SubscriberForm()

    context = {
        'shop': shop,
        'form': form,
    }
    return render(request, 'subscribers/subscribe.html', context)


def unsubscribe_view(request, qr_token):
    shop = get_object_or_404(ShopOwnerProfile, qr_token=qr_token)

    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            raw_phone = form.cleaned_data['phone_number']

            subscribers = Subscriber.objects.filter(shop=shop, is_active=True)

            for subscriber in subscribers:
                if subscriber.matches_phone_number(raw_phone):
                    subscriber.is_active = False
                    subscriber.save()
                    messages.success(request, 'You have been unsubscribed successfully.')
                    return redirect('unsubscribe_success')

            messages.error(request, 'No active subscription found for that phone number.')
    else:
        form = UnsubscribeForm()

    context = {
        'shop': shop,
        'form': form,
    }
    return render(request, 'subscribers/unsubscribe.html', context)


def subscribe_success(request):
    return render(request, 'subscribers/subscribe_success.html')


def unsubscribe_success(request):
    return render(request, 'subscribers/unsubscribe_success.html')