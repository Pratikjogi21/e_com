from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from UserApp.models import *
from Host_Admin.models import *

@login_required
def product_list(request):
    products = Product.objects.all() 
    cart_items = AddToCard.objects.filter(user=request.user)
    q=0

    for item in cart_items:
        q += item.quantity 
    
    return render(request, 'product_list.html', {'products': products,'q': q})