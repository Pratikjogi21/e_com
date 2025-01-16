from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from UserApp.models import *
from Host_Admin.models import *
from django.contrib import messages


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} units of {product.product_name} are available.")
        return redirect('/product_list') 
    
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'product_name': product.product_name,
            'product_price': float(product.product_price),  
            'quantity': quantity,
        }

    request.session['cart'] = cart

    messages.success(request, f"{product.product_name} added to your cart.")
    return redirect('/cart') 



@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_price = 0

    for product_id, details in cart.items():
        product_name = details['product_name']
        product_price = details['product_price']
        quantity = details['quantity']
        
        total_item_price = product_price * quantity
        total_price += total_item_price 
        
        cart_items.append({
            'product_id': product_id,
            'product_name': product_name,
            'product_price': product_price,
            'quantity': quantity,
            'total_item_price': total_item_price,
        })

    return render(request, 'card_detail.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart 
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")

    return redirect('/cart')
