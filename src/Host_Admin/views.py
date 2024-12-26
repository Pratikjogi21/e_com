from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

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

        if product_id and product_name and product_image and product_price:
            product = Product(
                product_id=product_id,
                product_name=product_name,
                product_image=product_image,
                product_price=product_price
            )
            product.save() 

            return render(request,'add_product.html') 
        else:
            return render(request, 'add_product.html', {'error': 'All fields are required.'})

    return render(request, 'add_product.html')