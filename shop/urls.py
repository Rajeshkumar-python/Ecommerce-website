# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),  # ✅ This is the correct nam
#     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.cart_view, name='cart'),
#     path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart'),
#     path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('order-success/<str:order_number>/', views.order_success, name='order_success'),
#     path('my-orders/', views.my_orders, name='my_orders'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # Home and Products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Checkout (placeholder for now)
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    # Checkout and Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('logout/', views.logout_view, name='logout'),
]