from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from Host_Admin.models import Product
from UserApp.models import AddToCard
from django.contrib import messages
from Host_Admin.models import Order
from django.db import transaction

 
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
    cart_items = AddToCard.objects.filter(user=request.user)
    q=0

    for item in cart_items:
        q += item.quantity 
        # print(q)
    
    return render(request, 'product_list.html', {'products': products,'q': q})

#--------------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} units of {product.product_name} are available.")
        return redirect('/product_list')

    # product.stock -= quantity
    # product.save() 

    cart_item, created = AddToCard.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity 

    cart_item.save()

    messages.success(request, f"{product.product_name} added to your cart.")
    return redirect('/cart')




@login_required
def cart_detail(request):
    cart_items = AddToCard.objects.filter(user=request.user)
    # print(cart_items)
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, 'card_detail.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(AddToCard, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('/cart')

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  
        total_price = product.product_price * quantity 
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        product.stock -= quantity
        product.save()

        return render(request, 'order_confirmation.html', {'order': order})

    return render(request, 'order_page.html', {'product': product})




@login_required
def purchase_cart(request):
    if request.method == 'POST':
        cart_items = AddToCard.objects.filter(user=request.user)

        if not cart_items.exists():
            return render(request, 'card_detail.html', {
                'cart_items': cart_items,
                'total': 0,
                'error_message': 'Your cart is empty!',
            })

        try:
            # Process the order
            for item in cart_items:
                order = Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price(),
                )
                item.product.stock_quantity -= item.quantity 
                item.product.save()

            cart_items.delete()

            return redirect('order_confirmation', order_id=order.id)

        except Exception as e:
            return render(request, 'card_detail.html', {
                'cart_items': cart_items,
                'total': sum(i.total_price() for i in cart_items),
                'error_message': f"An error occurred: {str(e)}",
            })

    return render(request, 'card_detail.html')