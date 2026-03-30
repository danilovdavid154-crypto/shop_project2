from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from catalog.cart import build_cart_context, clear_cart, get_cart
from catalog.models import Product

from .forms import OrderCreateForm
from .models import Order, OrderItem


@transaction.atomic
def checkout_view(request):
    cart_context = build_cart_context(request)
    cart_items = cart_context['cart_items']

    if not cart_items:
        messages.warning(request, 'Корзина пуста. Добавьте товары перед оформлением заказа.')
        return redirect('catalog:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            product_ids = [item['product'].id for item in cart_items]
            products_by_id = Product.objects.select_for_update().filter(id__in=product_ids, is_active=True)
            products_map = {product.id: product for product in products_by_id}

            stock_errors = []
            for item in cart_items:
                product = products_map.get(item['product'].id)
                if product is None or item['quantity'] > product.stock:
                    stock_errors.append(item['product'].name)

            if stock_errors:
                messages.error(
                    request,
                    'Некоторые товары недоступны в нужном количестве. Проверьте корзину: '
                    + ', '.join(stock_errors),
                )
                session_cart = get_cart(request)
                for product in products_by_id:
                    key = str(product.id)
                    if key in session_cart and session_cart[key] > product.stock:
                        session_cart[key] = product.stock
                request.session.modified = True
                return redirect('catalog:cart_detail')

            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart_items:
                product = products_map[item['product'].id]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
                product.stock -= item['quantity']
                product.save(update_fields=['stock'])

            clear_cart(request)
            messages.success(request, f'Заказ №{order.id} успешно оформлен.')
            if request.user.is_authenticated:
                return redirect('orders:my_orders')
            return redirect('catalog:product_list')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name() or request.user.username
        form = OrderCreateForm(initial=initial)

    context = {
        'form': form,
        **cart_context,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/my_orders.html', {'orders': orders})
