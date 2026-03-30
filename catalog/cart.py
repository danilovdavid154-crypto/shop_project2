from decimal import Decimal

from .models import Product


CART_SESSION_KEY = 'cart'


def get_cart(request):
    cart = request.session.get(CART_SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        request.session[CART_SESSION_KEY] = cart
        request.session.modified = True
    return cart


def set_cart_quantity(request, product, quantity):
    cart = get_cart(request)
    product_id = str(product.id)

    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = min(quantity, product.stock)

    request.session.modified = True


def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True


def build_cart_context(request):
    cart = get_cart(request)
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    items = []
    total_sum = Decimal('0.00')
    total_quantity = 0

    for product in products:
        quantity = min(cart.get(str(product.id), 0), product.stock)
        if quantity <= 0:
            cart.pop(str(product.id), None)
            continue

        item_total = product.price * quantity
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            }
        )
        total_sum += item_total
        total_quantity += quantity

    request.session.modified = True
    return {
        'cart_items': items,
        'cart_total_sum': total_sum,
        'cart_total_positions': len(items),
        'cart_total_quantity': total_quantity,
    }
