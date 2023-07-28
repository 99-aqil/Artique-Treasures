from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Product, User
from .forms import AdminProductForm, ProductForm


def loginView(request):
    return render(request, 'login.html')

def registrationView(request):
    return render(request, 'register.html')

def logoutView(request):
    return redirect('login-page')


def admin_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products-admin-view')
    else:
        form = ProductForm(instance=product)
    return render(request, 'adminEdit.html', {'form': form})



"""********************************************** C R U D **********************************************"""

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'view.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products-seller-view')
    else:
        form = ProductForm()
    return render(request, {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products-seller-view')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit.html', {'form': form})

def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return redirect('products-seller-view')



"""********************************************** C A R T **********************************************"""

def add_to_cart(request, product_id, user_id):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    user = User.objects.get(pk=user_id)
    # messages.success(request, f"{product.name} added to cart!")
    return redirect('product-detail', product_id=product_id, user_id=user_id)

def cart_view(request, pk=None):
    cart_item_ids = request.session.get('cart', [])
    cart_items = Product.objects.filter(pk__in=cart_item_ids)
    total_price = sum(item.price for item in cart_items)
    user = User.objects.get(pk=pk)

    context = {
        'user': user,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    print(context)
    return render(request, 'cart.html', context)

def clear_cart(request, pk=None):
    request.session['cart'] = []
    return redirect('cart-view', pk)

def checkout(request):
    return render(request, 'checkout.html')