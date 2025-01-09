from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from UserApp.models import *
from Host_Admin.models import *

@login_required
def Cart_review(request,user_id):
    items = AddToCard.objects.filter(user_id=user_id)
    total = sum(item.total_price() for item in items)
    print(items)
    pd ={
        'items':items,
        'total':total
    }
    return render(request,"cart_review.html",pd) 



def confirm_order_cart(request):
    if request.method == 'POST':
        cart_items = AddToCard.objects.filter(user=request.user)
        orders = []
        if cart_items.exists():
            insufficient_stock_items = []
            for item in cart_items:
                if item.product.stock >= item.quantity: 
                    total_price = item.quantity * item.product.product_price
                    order = Order.objects.create(
                        user=request.user,
                        product=item.product,
                        quantity=item.quantity,
                        total_price=total_price
                    )
                    item.product.stock -= item.quantity
                    item.product.save()
                    orders.append(order)
                else:
                    insufficient_stock_items.append(item.product.product_name)

            if insufficient_stock_items:
                error_message = f"Insufficient stock for the following items: {', '.join(insufficient_stock_items)}"
                return render(request, "cart_review.html", {'error': error_message, 'items': cart_items})

            cart_items.delete() 
            return render(request, "order_confirmation_cart.html", {'orders': orders})

    return render(request, "cart_review.html")

