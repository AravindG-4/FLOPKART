from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .decorators import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from application.models import *
# Create your views here.

# @login_required(login_url='login')
def home(request):
    return render(request, "home.html")

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin_templates/admin.html')
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
def seller_details(request):

    user_data = request.session.get('new_user_data')
    
    if not user_data:
        return redirect('user_management')
    
    if request.method == "POST":
        brand_name = request.POST.get('brand_name').strip()
        brand_description = request.POST.get('brand_description').strip()
        brand_logo = request.FILES.get('brand_logo')
        top_categories_1 = request.POST.get('top_categories_1').strip()
        top_categories_2 = request.POST.get('top_categories_2').strip()
        top_subCategories_1 = request.POST.get('top_subCategories_1').strip()
        top_subCategories_2 = request.POST.get('top_subCategories_2').strip()
        
        # Create the new user object
        new_user = User(username=user_data['username'], email=user_data['email'])
        new_user.set_password(user_data['password'])
        new_user.save()
        
        group = Group.objects.get(name='Seller')
        new_user.groups.add(group)
        
        # Save the brand
        brand = Brand(user=new_user, name=brand_name, description=brand_description, logo=brand_logo)
        brand.save()
        
        if top_categories_1:
            category1 = Category.objects.get(id=top_categories_1)
            brand.top_categories.add(category1)
        if top_categories_2:
            category2 = Category.objects.get(id=top_categories_2)
            brand.top_categories.add(category2)
            
        if top_subCategories_1:
            sub_category1 = SubCategory.objects.get(id=top_subCategories_1)
            brand.top_subCategories.add(sub_category1)
        if top_subCategories_2:
            sub_category2 = SubCategory.objects.get(id=top_subCategories_2)
            brand.top_subCategories.add(sub_category2)
        
        brand.save()
        
        # Clear the session data
        del request.session['new_user_data']
        
        messages.success(request, "User registered successfully ✅")
        return redirect('user_management')
    
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, 'admin_templates/seller_details.html', {'categories': categories, 'subcategories': subcategories})


@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def user_management(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        uname = request.POST.get('uname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        conf_password = request.POST.get('conf_password').strip()
        role = request.POST.get('role')
        
        try:
            user = User.objects.get(username=uname)
            messages.success(request, "Username already exists ⚠️")
            return redirect('user_management')
        
        except User.DoesNotExist:
            if password != conf_password:
                messages.success(request, "Passwords do not match ⚠️")
                return redirect('user_management')
            
            if role == 'Admin':
                new_user = User.objects.create_user(uname, email, password)
                new_user.is_superuser = True
                new_user.is_staff = True
                new_user.save()
            elif role == 'Seller':
                request.session['new_user_data'] = {
                    'username': uname,
                    'email': email,
                    'password': password,
                }
                return redirect('seller_details')
            else:
                new_user = User.objects.create_user(uname, email, password)
                new_user.save()

            messages.success(request, "User registered successfully ✅")
            return redirect('user_management')
    
    users = User.objects.all()
    group = get_object_or_404(Group, name='Seller')
    group_users = group.user_set.all()
    return render(request, 'admin_templates/user_management.html', {'users': users, 'group_users': group_users})
  
@csrf_exempt
@require_POST
def delete_user(request):
    print("Delete user view called")
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': True, 'message': 'User deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def admin_analytics(request):
    users = len(User.objects.all())
    orderlogs = len(OrderLog.objects.all())
    products = Product.objects.all()
    productslen = len(products)
    priceWorth = 0
    for product in products:
        priceWorth+=product.actual_price
    
    return render(request, 'admin_templates/analytics.html', {'users': users, 'orderlogs': orderlogs,
                                                              'products': productslen, 'priceWorth': priceWorth})

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def product_management(request):
    
    products = Product.objects.all()
    product_with_images = []

    for product in products:
        main_image = ProductImage.objects.filter(product=product, is_main=True).first()
        product_with_images.append({
            'product': product,
            'main_image': main_image
        })

    return render(request, 'admin_templates/product_management.html', {'product_with_images': product_with_images})
    

    
@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def add_product(request):
    if request.method == "POST":
        try:
            pname = request.POST.get('pname').strip()
            brand = request.POST.get('brand').strip()
            category = request.POST.get('category').strip()
            subcategory = request.POST.get('subcategory').strip()
            price = float(request.POST.get('price').strip())
            discount = float(request.POST.get('discount').strip())
            stock_xs = int(request.POST.get('stock_xs').strip())
            stock_s = int(request.POST.get('stock_s').strip())
            stock_m = int(request.POST.get('stock_m').strip())
            stock_l = int(request.POST.get('stock_l').strip())
            stock_xl = int(request.POST.get('stock_xl').strip())
            stock_xxl = int(request.POST.get('stock_xxl').strip())
            color = request.POST.get('color').strip().lower()
            description = request.POST.get('description').strip()
            main_image = request.FILES.get('main_image')
            sub_image1 = request.FILES.get('sub_image1')
            sub_image2 = request.FILES.get('sub_image2')
            
            available_stock = stock_xs + stock_s + stock_m + stock_l + stock_xl + stock_xxl
            brand = Brand.objects.get(id=brand)
            category = Category.objects.get(id=category)
            subcategory = SubCategory.objects.get(id=subcategory)
        
            product = Product(name=pname, description=description, available_stock=available_stock,
                            XS_stock=stock_xs, S_stock=stock_s, M_stock=stock_m, L_stock=stock_l,
                            XL_stock=stock_xl, XXL_stock=stock_xxl, colour=color, actual_price=price,
                            discount=discount, created_by=request.user, brand=brand, category=category, sub_category=subcategory
                            )
            product.save()
            
            
            ProductImage.objects.create(product=product, image=main_image, is_main=True)
            
            ProductImage.objects.create(product=product, image=sub_image1)
            
            ProductImage.objects.create(product=product, image=sub_image2)
            return redirect('product_management')
        except Exception as e:
            print(e)
            return redirect('product_management')
    brands = Brand.objects.all()
    categories = Category.objects.all()
    subCategories = SubCategory.objects.all()
    return render(request, 'admin_templates/add_product.html', {'brands':brands, 'categories':categories, 'subCategories':subCategories})
    
@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def update_product(request):
    
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        pname = request.POST.get('pname').strip()
        brand = request.POST.get('brand').strip()
        category = request.POST.get('category').strip()
        subcategory = request.POST.get('subcategory').strip()
        price = float(request.POST.get('price').strip())
        discount = float(request.POST.get('discount').strip())
        stock_xs = int(request.POST.get('stock_xs').strip())
        stock_s = int(request.POST.get('stock_s').strip())
        stock_m = int(request.POST.get('stock_m').strip())
        stock_l = int(request.POST.get('stock_l').strip())
        stock_xl = int(request.POST.get('stock_xl').strip())
        stock_xxl = int(request.POST.get('stock_xxl').strip())
        color = request.POST.get('color').strip().lower()
        description = request.POST.get('description').strip()
        main_image = request.FILES.get('main_image')
        sub_image1 = request.FILES.get('sub_image1')
        sub_image2 = request.FILES.get('sub_image2')
        
        available_stock = stock_xs + stock_s + stock_m + stock_l + stock_xl + stock_xxl
        brand = Brand.objects.get(id=brand)
        category = Category.objects.get(id=category)
        subcategory = SubCategory.objects.get(id=subcategory)
        
        product = Product.objects.get(id=product_id)
    
        product.name = pname
        product.description = description
        product.available_stock = available_stock
        product.XS_stock = stock_xs
        product.S_stock = stock_s
        product.M_stock = stock_m
        product.L_stock = stock_l
        product.XL_stock = stock_xl
        product.XXL_stock = stock_xxl
        product.colour = color
        product.actual_price = price
        product.discount = discount
        product.brand = brand
        product.category = category
        product.sub_category = subcategory
        product.save()

        
        if main_image:
            try:
                main_image_instance = ProductImage.objects.get(product=product, is_main=True)
                main_image_instance.image = main_image
                main_image_instance.save()
                print("main image")
            except:
                ProductImage.objects.create(product=product, image=main_image, is_main=True)

  
        sub_image_ids = [1, 2]
        for i, sub_image in enumerate([sub_image1, sub_image2], start=1):
            if sub_image:
                try:
                    sub_image_instance = ProductImage.objects.filter(product=product, is_main=False)[i-1]
                    sub_image_instance.image = sub_image
                    sub_image_instance.save()
                    print("sub")
                except IndexError:
                    ProductImage.objects.create(product=product, image=sub_image, is_main=False)
        return redirect('product_management')
    
    if request.GET.get('id'):
        product_id = request.GET.get('id')
        product = Product.objects.get(id=product_id)
        print(product.id)
        brands = Brand.objects.all()
        categories = Category.objects.all()
        subCategories = SubCategory.objects.all()
        product_images = ProductImage.objects.filter(product=product)
        return render(request, 'admin_templates/update_product.html', {'product':product,'brands':brands, 'categories':categories, 'subCategories':subCategories, 'product_images':product_images})
    
    return redirect('product_management')

@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def orderlogs(request):
    orderlogs = OrderLog.objects.all()
    return render(request, 'admin_templates/orderlogs.html', {'orderlogs': orderlogs})
    
@login_required(login_url='login')
@allowed_user(allowed_roles=['superuser'])
def orderform(request):
    if request.method == "POST":
      try:  
        product = Product.objects.get(name='OTTO White Striped Shirt')
        address = request.POST.get('address')
        phone = str(request.POST.get('phone'))
        quantity = int(request.POST.get('quantity'))
        print(product,address,phone,quantity)
        
        order = OrderLog.objects.create(user=request.user, product=product,
                                        address=address, phone=phone, quantity=quantity,
                                        total_price=product.available_price*quantity)
        print(order.id)
        return redirect('orderlogs')
      except Exception as e:
            print(e)
            return redirect('orderform')
        
    return render(request, 'admin_templates/orderform.html')