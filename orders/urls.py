from django.urls import path

from .views import checkout_view, my_orders_view


app_name = 'orders'


urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('my-orders/', my_orders_view, name='my_orders'),
]
