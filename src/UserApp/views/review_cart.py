from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from UserApp.models import *
from Host_Admin.models import *
from django.http import JsonResponse
from django.db import transaction
import uuid
from decimal import Decimal
from django.shortcuts import render



@login_required
def Cart_review(request, user_id):
    cart = request.session.get('cart', {})

    if not cart:
        return render(request, "cart_review.html", {'message': 'Your cart is empty.'})

    total = Decimal('0.00')

    items = []

    for product_id, details in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue  

        quantity = details.get('quantity', 0)

        quantity = int(quantity)

        product_price = Decimal(str(product.product_price))

        product_total_price = product_price * quantity
        total += product_total_price

        items.append({
            'product_name': product.product_name,
            'product_price': product_price,
            'quantity': quantity,
            'total_price': product_total_price
        })

    return render(request, "cart_review.html", {'items': items, 'total': total})







def create_order(request):
 
    user = request.user
    cart = request.session.get('cart', {})

    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    order_id = str(uuid.uuid4())
    total_price = Decimal('0.00') 

    order = Order.objects.create(user=user, order_id=order_id, total_price=total_price)

    for product_id, details in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with ID {product_id} not found'}, status=400)

        product_price = Decimal(str(product.product_price)) 
        quantity = int(details.get('quantity', 1)) 

        if product.stock < quantity:
            return JsonResponse({'error': f'Not enough stock for {product.product_name}'}, status=400)

        total_price += product_price * quantity

        OrderItem.objects.create(
            order=order,
            product_name=product.product_name,  
            product_price=product_price,
            quantity=quantity
        )

        product.stock -= quantity
        product.save()

    order.total_price = total_price
    order.save()

    request.session['cart'] = {}

    return render(request, "order_confirmation_cart.html", {'order': order})


def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all() 
    print(order)
    print(items)
    return render(request, 'orders/order_details.html', {'order': order, 'items': items})


def list_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    print(orders)
    return render(request, 'list_orders.html', {'orders': orders})
