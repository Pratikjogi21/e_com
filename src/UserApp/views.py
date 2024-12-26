from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from Host_Admin.models import Product



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