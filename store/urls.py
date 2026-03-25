from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),

    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path(
        'category/<slug:category_slug>/<slug:product_slug>/',
        views.product_detail,
        name='product_detail'
    ),

    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('subscribe/', views.subscribe_landing, name='subscribe_landing'),
    path('subscribe/<str:qr_token>/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscription_success, name='subscription_success'),
]