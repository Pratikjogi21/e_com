from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Host_Admin.views.order_views import order_detail
from UserApp.models import *
from Host_Admin.models import *

 
@login_required
def create_order_user(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = Profile.objects.get(user=request.user)


    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  
        total_price = product.product_price * quantity 
        order = Order.objects.create(
            user=request.user,
            
            total_price=total_price
        )
        product.stock -= quantity
        product.save()

        return render(request, 'order_confirmation.html', {'order': order,'order_id': order.order_id})

    return render(request, 'order_page.html', {'product': product,'profile': profile})