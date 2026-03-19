from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),

    # Password reset
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('reset-password/', views.resetPassword, name='resetPassword'),

    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<str:order_number>/', views.order_detail, name='order_detail'),
]