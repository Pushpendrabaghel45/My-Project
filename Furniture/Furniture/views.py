from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from account.models import *
# from django.contrib.auth.decorators import login_required
# from .models import Product

# from products.models import Product, Category
from django.contrib.auth import logout
# Create your views here.
def home(request):
    context = {
        'hero': HomeHero.objects.filter(is_active=True).first(),
        'counters': HomeCounter.objects.all(),
        'categories': HomeCategory.objects.all(),
        'products': HomeProduct.objects.filter(is_active=True),
        'banner': HomeBanner.objects.first(),
        'testimonial': Testimonial.objects.first(),
    }
    return render(request, 'index.html', context)
        
def pages(request):
    return render(request, 'pages.html')

def shop(request):
    return render(request, 'shop.html')
       

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            request.session['user_logged_in'] = True
            request.session['username'] = username
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')




def admin_logout(request):
    print("outside chala")
    logout(request)
    request.session.flush()
    return redirect('home')
