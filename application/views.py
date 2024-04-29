from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

# @login_required(login_url='login')
def home(request):
    return render(request, "home.html")

def user_login(request):
    
    try:
        if user.is_authenticated:
            messages.success(request, "User already logged in⚠️")
            return redirect('home')
    except:  
        
        if request.method=='POST':
            username=request.POST.get('uname')
            password=request.POST.get('password')
        
        
            # if request.user.is_authenticated:
            #     messages.success(request, "User already logged in⚠️")
            #     return redirect('home')
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request, "Invalid credentials ⚠️")
            return redirect('user_login')

    return render (request,'login.html', {'user': request.user})
    

def signup(request):
    
    if request.method=='POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        
        try:
            user = User.objects.get(username=uname)
            messages.success(request, "Username already exists ⚠️")
            return redirect('signup')
        except:
            pass
        
        
        if password != conf_password:        
                messages.success(request, "Passwords do not match ⚠️")
                return redirect('signup')
                
        new_user = User.objects.create_user(uname, email, password)
        new_user.save()

        messages.success(request, "User registered successfully ✅")
        return redirect('login')
        
    
    return render(request, "signup.html")

def user_logout(request):
    logout(request)
    return redirect('login')