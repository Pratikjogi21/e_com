from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from e_app.models import *

@login_required
def userProfile(request):
    return render(request,"profile.html",{'m':request.user}) 
    