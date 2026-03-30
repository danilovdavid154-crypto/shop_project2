from .cart import build_cart_context


def cart_summary(request):
    return build_cart_context(request)
