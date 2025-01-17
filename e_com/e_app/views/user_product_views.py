from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from e_app.models import *
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = Product.objects.all()
    
    cart = request.session.get('cart', {})

    q = sum(item['quantity'] for item in cart.values())

    return render(request, 'product_list.html', {'products': products, 'q': q})
