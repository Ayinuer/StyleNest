from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category


def home(request):
    products = Product.objects.filter(is_available=True)[:8]

    context = {
        'products': products,
    }
    return render(request, 'store/home.html', context)


def store(request, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by('product_name')
    products_count = products.count()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True,
    )

    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)