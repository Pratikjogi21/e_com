from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product,Order

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


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = 1  # Default quantity for "Buy Now"
    
    # Ensure the product has enough stock
    if product.stock < quantity:
        messages.error(request, f"Sorry, {product.product_name} is out of stock!")
        return redirect('product_list')  # Redirect to the product listing

    # Create an order
    total_price = quantity * product.product_price
    order = Order.objects.create(
        user=request.user,
        product=product,
        quantity=quantity,
        total_price=total_price
    )

    # Reduce stock
    product.stock -= quantity
    product.save()

    messages.success(request, f"You have successfully purchased {product.product_name}!")
    return redirect('order_detail', order_id=order.id)