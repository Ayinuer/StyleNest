from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

from accounts.models import ShopOwnerProfile
from category.models import Category
from .models import Product, ReviewRating, Subscriber, Wishlist
from .forms import ReviewForm


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

    reviews = ReviewRating.objects.filter(
        product=single_product,
        status=True
    ).order_by('-created_at')

    average_review = reviews.aggregate(average=Avg('rating'))
    review_count = reviews.aggregate(count=Count('id'))

    context = {
        'single_product': single_product,
        'product_gallery': [],
        'reviews': reviews,
        'average_review': average_review,
        'review_count': review_count,
    }
    return render(request, 'store/product_detail.html', context)


@login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER', 'store')

    if request.method == 'POST':
        review_text = request.POST.get('review', '')
        rating_value = request.POST.get('rating')

        try:
            review = ReviewRating.objects.get(user=request.user, product_id=product_id)
            review.review = review_text
            review.rating = rating_value
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()
            messages.success(request, 'Your review has been updated successfully.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            ReviewRating.objects.create(
                product_id=product_id,
                user=request.user,
                subject='',
                review=review_text,
                rating=rating_value,
                ip=request.META.get('REMOTE_ADDR'),
            )
            messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect(url)

    return redirect(url)


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, 'Product added to wishlist.')
    else:
        messages.info(request, 'This product is already in your wishlist.')

    return redirect(request.META.get('HTTP_REFERER', product.get_url()))


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)


def subscribe_landing(request):
    return render(request, 'store/subscribe_landing.html')


def subscribe(request, qr_token):
    shop = get_object_or_404(ShopOwnerProfile, qr_token=qr_token)

    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        birth_month = request.POST.get('birth_month')

        if email:
            Subscriber.objects.create(
                shop=shop,
                email=email,
                phone_number=phone_number,
                birth_month=birth_month
            )
            messages.success(request, 'You subscribed successfully!')
            return redirect('subscription_success')

    context = {
        'shop': shop,
    }
    return render(request, 'store/subscribe.html', context)


def subscription_success(request):
    return render(request, 'store/subscription_success.html')