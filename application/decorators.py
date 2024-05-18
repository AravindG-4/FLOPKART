from django.shortcuts import render, redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_user(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            
            try:
                if 'superuser' in allowed_roles and request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                
                elif any(role in allowed_roles for role in request.user.groups.values_list('name', flat=True)):
                    return view_func(request, *args, **kwargs)
                
                else:
                    return redirect('home')
            except:
                return redirect('home')
            
        return wrapper_func
    return decorator
