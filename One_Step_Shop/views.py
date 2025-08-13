from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django import forms
from django.http import JsonResponse
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

def all_products(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.filter(parent__isnull=True).order_by('name')

    if query:
        search_results = Product.objects.filter(name__icontains=query)
        return render(request, 'One_Step_Shop/products.html', {
            'categories': categories,
            'query': query,
            'search_results': search_results,
            'search_mode': True
        })
    
    categories_with_products = []
    for category in categories:
        subcat_ids = category.subcategories.values_list('id', flat=True)
        cat_and_subcat_ids = list(subcat_ids) + [category.id]
        cat_products = Product.objects.filter(category_id__in=cat_and_subcat_ids)
        categories_with_products.append((category, cat_products))

    return render(request, 'One_Step_Shop/products.html', {
        'categories_with_products': categories_with_products,
        'query': query,
        'search_mode': False
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('all_products')
    else:
        form = ProductForm()
    return render(request, 'One_Step_Shop/add_product.html', {'form': form})

@login_required
@require_POST
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Added to cart'})
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'One_Step_Shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

@login_required
@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    messages.success(request, "Cart cleared.")
    return redirect('view_cart')

@login_required
@require_POST
def update_cart_quantity(request, product_id):
    action = request.POST.get('action')
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)] += 1
        elif action == 'decrease':
            cart[str(product_id)] = max(cart[str(product_id)] - 1, 1)
        request.session['cart'] = cart
    return redirect('view_cart')

@login_required
@require_POST
def buy_now(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('checkout')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        request.session['cart'] = {}
        return redirect('thank_you')

    return render(request, 'One_Step_Shop/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def thank_you(request):
    return render(request, 'One_Step_Shop/thank_you.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('all_products')
        messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'One_Step_Shop/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please login.")
            return redirect('login')
        messages.error(request, "Registration failed.")
    else:
        form = UserCreationForm()
    return render(request, 'One_Step_Shop/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')