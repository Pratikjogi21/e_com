from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Host_Admin.models import *
from UserApp.views import *


def add_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('media')
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

def update_product(request, product_id):
    try:
        pd = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect("/product_not_found") 
    
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('product_image')
        product_price = request.POST.get('product_price')
        stock = request.POST.get('stock')
        
        if product_name: 
            pd.product_name = product_name
        if product_image: 
            pd.product_image = product_image
        if product_price:
            pd.product_price = product_price
        if stock is not None: 
            pd.stock = stock
        
        pd.save()
        return redirect("/admin_product_list")
    
    return render(request, "edit_product.html", {'m': pd})

