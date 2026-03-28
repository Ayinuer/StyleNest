from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import ShopOwnerProfile
from store.models import Subscriber
from campaigns.models import Campaign


def get_shop_profile(user):
    return ShopOwnerProfile.objects.filter(user=user).first()


# AUTH
def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user = None

        if '@' in email_or_username:
            try:
                user_obj = User.objects.get(email=email_or_username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid login details.')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not shop_name or not username or not password:
            messages.error(request, 'Shop name, username, and password are required.')
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        ShopOwnerProfile.objects.create(
            user=user,
            shop_name=shop_name,
            phone=phone
        )

        login(request, user)
        messages.success(request, 'Shop account created successfully.')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# DASHBOARD
@login_required
def dashboard(request):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        messages.error(request, 'No shop profile found.')
        return redirect('login')

    total_subscribers = Subscriber.objects.filter(shop=shop_profile).count()
    active_subscribers = Subscriber.objects.filter(shop=shop_profile, is_active=True).count()
    inactive_subscribers = Subscriber.objects.filter(shop=shop_profile, is_active=False).count()

    campaigns = Campaign.objects.filter(shop=shop_profile)
    total_campaigns = campaigns.count()
    total_delivered = sum(c.delivered_count for c in campaigns)

    context = {
        'shop_profile': shop_profile,
        'total_subscribers': total_subscribers,
        'active_subscribers': active_subscribers,
        'inactive_subscribers': inactive_subscribers,
        'total_campaigns': total_campaigns,
        'total_delivered': total_delivered,
    }
    return render(request, 'accounts/dashboard.html', context)


# PROFILE
@login_required
def edit_profile(request):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        return redirect('dashboard')

    if request.method == 'POST':
        shop_profile.shop_name = request.POST.get('shop_name', '').strip()
        shop_profile.phone = request.POST.get('phone', '').strip()
        request.user.email = request.POST.get('email', '').strip()

        shop_profile.save()
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('edit_profile')

    return render(request, 'accounts/edit_profile.html', {
        'shop_profile': shop_profile,
    })


@login_required
def change_password(request):
    return render(request, 'accounts/change_password.html')


# CAMPAIGNS
@login_required
def compose_message(request):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        return redirect('dashboard')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        template_type = request.POST.get('template_type', 'custom').strip()
        message_type = request.POST.get('message_type', 'sms').strip()
        message_body = request.POST.get('message_body', '').strip()
        scheduled_for = request.POST.get('scheduled_for', '').strip()

        if template_type == 'new_arrivals' and not message_body:
            message_body = 'New arrivals are now available. Visit our shop for the latest styles.'
        elif template_type == 'sale_alert' and not message_body:
            message_body = 'Sale alert! Limited-time offers are now live. Shop now before they end.'
        elif template_type == 'birthday_offer' and not message_body:
            message_body = 'Celebrate with us. Enjoy a special birthday offer this month.'

        active_subscribers = Subscriber.objects.filter(
            shop=shop_profile,
            is_active=True
        )
        total_recipients = active_subscribers.count()

        campaign = Campaign.objects.create(
            shop=shop_profile,
            title=title,
            template_type=template_type,
            message_type=message_type,
            message_body=message_body,
            total_recipients=total_recipients,
        )

        if scheduled_for:
            campaign.status = 'scheduled'
            campaign.scheduled_for = scheduled_for
            campaign.save()
            messages.success(request, 'Campaign scheduled successfully.')
        else:
            campaign.status = 'sent'
            campaign.sent_at = timezone.now()
            campaign.delivered_count = total_recipients
            campaign.failed_count = 0
            campaign.save()
            messages.success(request, 'Campaign sent successfully.')

        return redirect('message_history')

    return render(request, 'accounts/compose_message.html', {
        'shop_profile': shop_profile,
    })


@login_required
def message_history(request):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        return redirect('dashboard')

    campaigns = Campaign.objects.filter(shop=shop_profile).order_by('-created_at')

    return render(request, 'accounts/message_history.html', {
        'shop_profile': shop_profile,
        'campaigns': campaigns,
    })


# PASSWORD RESET PLACEHOLDERS
def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')


def resetPassword(request):
    return render(request, 'accounts/resetPassword.html')


# ORDERS PLACEHOLDERS
@login_required
def my_orders(request):
    return render(request, 'accounts/my_orders.html')


@login_required
def order_detail(request, order_number):
    return render(request, 'accounts/order_detail.html', {
        'order_number': order_number,
    })