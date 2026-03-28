from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/<int:shop_id>/', views.subscribe_view, name='subscribe_view'),
    path('unsubscribe/<int:shop_id>/', views.unsubscribe_view, name='unsubscribe_view'),
    path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
    path('unsubscribe/success/', views.unsubscribe_success, name='unsubscribe_success'),
]