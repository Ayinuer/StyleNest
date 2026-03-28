from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
    path('unsubscribe/success/', views.unsubscribe_success, name='unsubscribe_success'),

    path('subscribe/<str:qr_token>/', views.subscribe_view, name='subscribe'),
    path('unsubscribe/<str:qr_token>/', views.unsubscribe_view, name='unsubscribe'),
]