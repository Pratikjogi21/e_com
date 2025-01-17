from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from e_app.models import Host
from django.contrib.auth.hashers import make_password,check_password


# hashed_password = make_password('')
# print(hashed_password)

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Host.objects.get(username=username)

            if check_password(password, admin.password):
                
                request.session['is_logged_in'] = True
                request.session['username'] = username
                return redirect('/home') 
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/admin_login')
        
        except Host.DoesNotExist:
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
    
