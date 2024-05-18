from django.views.decorators.cache import cache_control
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .decorators import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

# @login_required(login_url='login')
def home(request):
    return render(request, "home.html")

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    
    if request.user.is_authenticated:
        # messages.success(request, "User already logged in⚠️")
        return redirect('home')
    
    else:
        if request.method=='POST':
            username=request.POST.get('uname')
            password=request.POST.get('password')
            
            try:  
                user=authenticate(request,username=username,password=password)
            
                if user is not None:
                    if user.is_superuser:
                        login(request,user)
                        messages.success(request, "Admin Access Provided!!")
                        return redirect('admin_dashboard')
                    login(request,user)
                    return redirect('home')
                else:
                    messages.success(request, "Invalid credentials ⚠️")
                    return redirect('user_login')
            except:
                return redirect('login')

        return render (request,'login.html')

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    elif request.method=='POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        
        try:
            user = User.objects.get(username=uname)
            messages.success(request, "Username already exists ⚠️")
            return redirect('signup')
        except:
            
            if password != conf_password:        
                    messages.success(request, "Passwords do not match ⚠️")
                    return redirect('signup')
                    
            new_user = User.objects.create_user(uname, email, password)
            new_user.save()

            messages.success(request, "User registered successfully ✅")
            return redirect('login')
    
    return render(request, "signup.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    messages.success(request, "User logged out successfully ✅")
    return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def user_management(request):
    
    if not request.user.is_authenticated:
            return redirect('login')
    
    if request.method=='POST':
        uname = request.POST.get('uname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        conf_password = request.POST.get('conf_password').strip()
        role = request.POST.get('role')
        
        try:
            user = User.objects.get(username=uname)
            messages.success(request, "Username already exists ⚠️")
            return redirect('user_management')
        
        except:    
            if password != conf_password:        
                    messages.success(request, "Passwords do not match ⚠️")
                    return redirect('user_management')
                    
            new_user = User.objects.create_user(uname, email, password)
            
            if role == 'Admin':
                new_user.is_superuser = True
                new_user.is_staff = True
                new_user.save()
            
            elif role == 'Seller':
                group = Group.objects.get(name = role)
                new_user.groups.add(group)
                
            new_user.save()

            messages.success(request, "User registered successfully ✅")
            return redirect('user_management')

    else:
        try:
            users = User.objects.all()
            group = get_object_or_404(Group, name='Seller')
            group_users = group.user_set.all()
            return render(request, 'user_management.html', {'users': users, 'group_users': group_users})
        except Exception as e:
            users = []
            return render(request, 'user_management.html',{'users': users})
  
    
@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def add_item(request):
    return render(request, 'add_item.html')
    
@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def update_item(request):
    return render(request, 'update_item.html')

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def remove_item(request):
    return render(request, 'remove_item.html')
    