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


    cart_item, created = AddToCard.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity 

    cart_item.save()

    messages.success(request, f"{product.product_name} added to your cart.")
    return redirect('/cart')




@login_required
def cart_detail(request):
    cart_items = AddToCard.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, 'card_detail.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(AddToCard, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('/cart')