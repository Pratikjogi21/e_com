from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from Host_Admin.models import Product
from UserApp.models import AddToCard
from django.contrib import messages



def registerView(request):
    if(request.user.is_authenticated):
        return redirect("/homeuser")
    if(request.method=="POST"):
        fname=request.POST.get('firstname')
        lname=request.POST.get('lastname')
        email=request.POST.get('email')
        pswd=request.POST.get('password')
        
        user = User.objects.create_user(username=email,first_name=fname,last_name=lname,password=pswd)
        user.save()
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        profile = Profile(user=user, address=address, city=city, state=state, postal_code=postal_code)
        profile.save()

        return redirect('/login')
    else:
        return render(request,"register.html")
    
@login_required
def homeView(request):
    return render(request,"home.html",{'m':request.user}) 

def loginView(request):
    if(request.user.is_authenticated):
        return redirect("/homeuser")
    if(request.method=="POST"):
       
        email=request.POST.get('email')
        pswd=request.POST.get('password')
        
        user=authenticate(username = email,password = pswd)
        if(user is not None):
            login(request,user)
            return redirect ('/homeuser')
        else:
            return redirect('/login')
    else:
        return render(request,"login.html")
@login_required
def logoutView(request):
    logout(request)
    return redirect('/login')

# -------------------------------------------------

def product_list(request):
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})

#--------------------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart_item, _ = AddToCard.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 0})
    # if not cart_item.pk:  
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.product_name} has been added to your cart!")
    return redirect('/cart')


@login_required
def cart_detail(request):
    cart_items = AddToCard.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'card_detail.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(AddToCard, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('/cart')

