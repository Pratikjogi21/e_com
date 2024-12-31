from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from Host_Admin.models import *
# from Host
from UserApp.views import *

USERNAME = "admin"
PASSWORD = "password123"

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == USERNAME and password == PASSWORD:
            request.session['is_logged_in'] = True
            request.session['username'] = username
            return redirect('/home') 
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/admin_login')
    return render(request, 'admin_login.html')

def admin_home(request):
    if not request.session.get('is_logged_in'):
        return redirect('/admin_login')  
    return render(request, 'admin_home.html', {'username': request.session.get('username')})

def logout_view(request):
    request.session.flush()
    return redirect('/admin_login')
# ------------------------------------------------------------


def add_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('product_image')
        product_price = request.POST.get('product_price')
        stock = request.POST.get('stock')


        if product_id and product_name and product_image and product_price and stock:
            product = Product(
                product_id=product_id,
                product_name=product_name,
                product_image=product_image,
                product_price=product_price,
                stock=stock

            )
            product.save() 

            return render(request,'add_product.html') 
        else:
            return render(request, 'add_product.html', {'error': 'All fields are required.'})

    return render(request, 'add_product.html')
# ------------------------------------------------------

def admin_product_list(request):
    products = Product.objects.all() 
    return render(request, 'admin_product_list.html', {'products': products})

#-----------------------------------
def delete_product(request,product_id):
    product = Product.objects.get(product_id = product_id)
    print(product)
    product.delete()
    return redirect('/admin_product_list')
#---------------------------------

def update_product(request,product_id):
    pd = Product.objects.get(id=product_id)
    if(request.method=="POST"):
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('product_image')
        product_price = request.POST.get('product_price')
        stock = request.POST.get('stock')

        pd.product_name = product_name
        if product_image:  
            pd.product_image = product_image
        pd.product_price = product_price
        pd.stock = stock
        pd.save()
        return redirect("/admin_product_list")
    else:
        return render(request,"edit_product.html",{'m':pd})

 





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
