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
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscription_success, name='subscription_success'),
]