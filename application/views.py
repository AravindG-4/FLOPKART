from django.shortcuts import render

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, "home.html")
