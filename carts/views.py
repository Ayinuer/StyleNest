from decimal import Decimal
import random
import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import Cart, CartItem
from store.models import Product
from orders_app.models import Order, OrderProduct


stripe.api_key = settings.STRIPE_SECRET_KEY


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def _generate_order_number():
    current_date = timezone.now().strftime('%Y%m%d')
    random_number = random.randint(1000, 9999)
    return f"SN{current_date}{random_number}"


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )

    return redirect('cart')


def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=Decimal('0.00'), quantity=0, cart_items=None):
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = total * Decimal('0.02')
        grand_total = total + tax

    except Cart.DoesNotExist:
        cart_items = []
        total = Decimal('0.00')
        quantity = 0
        tax = Decimal('0.00')
        grand_total = Decimal('0.00')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def checkout(request, total=Decimal('0.00'), quantity=0, cart_items=None):
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart')

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = total * Decimal('0.02')
        grand_total = total + tax

    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line_1 = request.POST.get('address_line_1', '').strip()
        address_line_2 = request.POST.get('address_line_2', '').strip()
        city = request.POST.get('city', '').strip()
        postcode = request.POST.get('postcode', '').strip()
        country = request.POST.get('country', '').strip()
        order_note = request.POST.get('order_note', '').strip()

        if not all([first_name, last_name, email, phone, address_line_1, city, postcode, country]):
            messages.error(request, 'Please complete all required checkout fields.')
            return redirect('checkout')

        request.session['checkout_data'] = {
            'full_name': f'{first_name} {last_name}',
            'email': email,
            'phone': phone,
            'address_line_1': address_line_1,
            'address_line_2': address_line_2,
            'city': city,
            'postcode': postcode,
            'country': country,
            'order_note': order_note,
        }

        return redirect('create_checkout_session')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'store/checkout.html', context)


def create_checkout_session(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        checkout_data = request.session.get('checkout_data')
        if not checkout_data:
            messages.error(request, 'Please complete the checkout form first.')
            return redirect('checkout')

        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': item.product.product_name,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=line_items,
            success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('checkout')),
        )

        return redirect(session.url, code=303)

    except Cart.DoesNotExist:
        messages.error(request, 'Cart not found.')
        return redirect('cart')
    except Exception as e:
        messages.error(request, f'Stripe checkout failed: {str(e)}')
        return redirect('checkout')


def payment_success(request):
    session_id = request.GET.get('session_id')
    checkout_data = request.session.get('checkout_data')

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        if not cart_items.exists():
            return render(request, 'store/payment_success.html')

        if not checkout_data:
            messages.error(request, 'Checkout information is missing.')
            return redirect('checkout')

        total = Decimal('0.00')
        quantity = 0

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = total * Decimal('0.02')
        grand_total = total + tax

        order_number = _generate_order_number()

        while Order.objects.filter(order_number=order_number).exists():
            order_number = _generate_order_number()

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number,
            full_name=checkout_data['full_name'],
            email=checkout_data['email'],
            phone=checkout_data['phone'],
            address_line_1=checkout_data['address_line_1'],
            address_line_2=checkout_data['address_line_2'],
            city=checkout_data['city'],
            postcode=checkout_data['postcode'],
            country=checkout_data['country'],
            order_total=total,
            tax=tax,
            shipping_cost=Decimal('0.00'),
            grand_total=grand_total,
            status='Processing',
            is_ordered=True,
        )

        for cart_item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=request.user if request.user.is_authenticated else None,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.price,
                ordered=True,
            )

            if cart_item.variations.exists():
                order_product.variations.set(cart_item.variations.all())

        CartItem.objects.filter(cart=cart).delete()
        cart.delete()

        request.session.pop('checkout_data', None)
        request.session['last_order_number'] = order.order_number
        request.session['stripe_session_id'] = session_id

    except Cart.DoesNotExist:
        pass

    return render(request, 'store/payment_success.html')