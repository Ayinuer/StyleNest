from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_page, name='billing_page'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]