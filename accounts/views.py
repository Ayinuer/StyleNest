from django.shortcuts import render, redirect


# AUTH
def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


def logout(request):
    return redirect('login')


# DASHBOARD
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


# PROFILE
def edit_profile(request):
    return render(request, 'accounts/edit_profile.html')


def change_password(request):
    return render(request, 'accounts/change_password.html')


# PASSWORD RESET
def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')


def resetPassword(request):
    return render(request, 'accounts/resetPassword.html')


# ORDERS
def my_orders(request):
    return render(request, 'accounts/my_orders.html')


def order_detail(request, order_number):
    return render(request, 'accounts/order_detail.html')