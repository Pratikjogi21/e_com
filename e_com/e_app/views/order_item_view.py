from django.shortcuts import render,redirect,get_object_or_404
from e_app.models import *
from django.shortcuts import render

def user_order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all()  # Retrieves all OrderItem objects related to this order
    return render(request, 'user_order_details.html', {'order': order, 'items': items})
