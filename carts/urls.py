from django.urls import path
from . import views

urlpatterns = [
    # CART
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

    # CHECKOUT
    path('checkout/', views.checkout, name='checkout'),

    # STRIPE
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success, name='payment_success'),
]