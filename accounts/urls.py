from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 🔥 Subscribers (IMPORTANT - you forgot this)
    path('subscribers/', views.subscribers_list, name='subscribers_list'),
    path('subscribers/toggle/<int:subscriber_id>/', views.subscriber_toggle_status, name='subscriber_toggle_status'),

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