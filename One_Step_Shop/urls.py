from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Cart URLs
    path('add-to-cart/<int:product_id>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('cart/', login_required(views.view_cart), name='view_cart'),
    path('remove-from-cart/<int:product_id>/', login_required(views.remove_from_cart), name='remove_from_cart'),
    path('cart/clear/', login_required(views.clear_cart), name='clear_cart'),
    path('cart/update/<int:product_id>/', login_required(views.update_cart_quantity), name='update_cart_quantity'),  # <-- Added here
    path('checkout/', login_required(views.checkout), name='checkout'),
    path('buy/<int:product_id>/', login_required(views.buy_now), name='buy_now'),

    # Product URLs
    path('add-product/', login_required(views.add_product), name='add_product'),
    path('thank-you/', login_required(views.thank_you), name='thank_you'),
]
