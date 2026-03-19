from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category


def home(request):
    products = Product.objects.filter(is_available=True).order_by('product_name')[:8]

    context = {
        'products': products,
    }
    return render(request, 'store/home.html', context)


def store(request, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by('product_name')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'products': products,
        'products_count': products.count(),
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
        'product_gallery': [],
    }
    return render(request, 'store/product_detail.html', context)


def subscribe(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        birth_month = request.POST.get('birth_month')

        # You can save phone_number and birth_month to a model later
        # For now, just redirect to success page
        return redirect('subscription_success')

    return render(request, 'store/subscribe.html')


def subscription_success(request):
    return render(request, 'store/subscription_success.html')