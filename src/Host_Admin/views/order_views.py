from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Host_Admin.models import *
from UserApp.views import *
from UserApp.models import *

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    profile = Profile.objects.get(user=request.user)
    print(profile)

    return render(request, 'order_detail.html', {'order': order,'profile': profile})


    #-----------------------

def vieworders(request):
    order = Order.objects.all()
    return render(request, 'all_orders.html', {'order': order})

    
def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}")
        return redirect('/view_orders')