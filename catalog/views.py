from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .cart import build_cart_context, get_cart, set_cart_quantity
from .models import Product


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    context = {
        'products': products,
        **build_cart_context(request),
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=slug,
        is_active=True,
    )
    context = {
        'product': product,
        **build_cart_context(request),
    }
    return render(request, 'catalog/product_detail.html', context)


def cart_detail(request):
    return render(request, 'catalog/cart.html', build_cart_context(request))


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if product.stock <= 0:
        messages.error(request, f'Товар "{product.name}" закончился.')
        return redirect(request.META.get('HTTP_REFERER', 'catalog:product_list'))

    cart = get_cart(request)
    product_key = str(product.id)
    current_quantity = cart.get(product_key, 0)

    if current_quantity >= product.stock:
        messages.warning(request, f'Нельзя добавить больше {product.stock} шт. товара "{product.name}".')
    else:
        set_cart_quantity(request, product, current_quantity + 1)
        messages.success(request, f'Товар "{product.name}" добавлен в корзину.')

    return redirect(request.META.get('HTTP_REFERER', 'catalog:product_list'))


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    set_cart_quantity(request, product, 0)
    messages.info(request, f'Товар "{product.name}" удален из корзины.')
    return redirect('catalog:cart_detail')


def cart_increase(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)
    current_quantity = cart.get(str(product.id), 0)

    if current_quantity >= product.stock:
        messages.warning(request, f'Нельзя добавить больше {product.stock} шт. товара "{product.name}".')
    else:
        set_cart_quantity(request, product, current_quantity + 1)

    return redirect('catalog:cart_detail')


def cart_decrease(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)
    current_quantity = cart.get(str(product.id), 0)
    set_cart_quantity(request, product, current_quantity - 1)
    return redirect('catalog:cart_detail')


def custom_page_not_found(request, exception):
    return render(request, 'catalog/404.html', status=404)
