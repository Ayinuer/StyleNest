from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

from .models import ShopOwnerProfile
from store.models import Subscriber


# =========================
# AUTH
# =========================

def login_view(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email')
        password = request.POST.get('password')

        # 🔥 Allow login via email OR username
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
        else:
            messages.error(request, 'Invalid login details.')

    return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# HELPER (VERY IMPORTANT)
# =========================

def get_shop_profile(user):
    return ShopOwnerProfile.objects.filter(user=user).first()


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    shop_profile = get_shop_profile(request.user)

    # ✅ FIX: no spam messages
    if not shop_profile:
        return redirect('login')

    total_subscribers = Subscriber.objects.filter(shop=shop_profile).count()
    active_subscribers = Subscriber.objects.filter(shop=shop_profile, is_active=True).count()
    inactive_subscribers = Subscriber.objects.filter(shop=shop_profile, is_active=False).count()

    context = {
        'shop_profile': shop_profile,
        'total_subscribers': total_subscribers,
        'active_subscribers': active_subscribers,
        'inactive_subscribers': inactive_subscribers,
    }

    return render(request, 'accounts/dashboard.html', context)


# =========================
# SUBSCRIBERS
# =========================

@login_required
def subscribers_list(request):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        return redirect('dashboard')

    subscribers = Subscriber.objects.filter(shop=shop_profile).order_by('-created_at')

    context = {
        'shop_profile': shop_profile,
        'subscribers': subscribers,
    }

    return render(request, 'accounts/subscribers_list.html', context)


@login_required
def subscriber_toggle_status(request, subscriber_id):
    shop_profile = get_shop_profile(request.user)

    if not shop_profile:
        return redirect('dashboard')

    subscriber = get_object_or_404(
        Subscriber,
        id=subscriber_id,
        shop=shop_profile
    )

    subscriber.is_active = not subscriber.is_active
    subscriber.save()

    if subscriber.is_active:
        messages.success(request, 'Subscriber activated successfully.')
    else:
        messages.success(request, 'Subscriber deactivated successfully.')

    return redirect('subscribers_list')


# =========================
# PROFILE
# =========================

@login_required
def edit_profile(request):
    shop_profile = get_shop_profile(request.user)

    return render(request, 'accounts/edit_profile.html', {
        'shop_profile': shop_profile,
    })


@login_required
def change_password(request):
    return render(request, 'accounts/change_password.html')


# =========================
# PASSWORD RESET
# =========================

def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')


def resetPassword(request):
    return render(request, 'accounts/resetPassword.html')


# =========================
# ORDERS
# =========================

@login_required
def my_orders(request):
    return render(request, 'accounts/my_orders.html')


@login_required
def order_detail(request, order_number):
    return render(request, 'accounts/order_detail.html', {
        'order_number': order_number,
    })