from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib import messages
from .forms import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
def register(request):
    if request.method == "POST":
        form = CreateFormRegister(request.POST)
        if form.is_valid():
            # Lấy dữ liệu từ form
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Tên tài khoản đã tồn tại')
                return render(request, "admin_page/register.html", {'form': form})
            if password1 != password2:
                form.add_error('password2', 'Mật khẩu không khớp nhau')
                return render(request, "admin_page/register.html", {'form': form})
            
            # Tạo user mới
            user = User.objects.create_user(username=username, password=password1, email=email)
            
            # Lưu các thông tin bổ sung
            customer = Customer.objects.create(user=user, name=name, address=address, phone=phone)
            
            # Chuyển hướng đến trang thành công hoặc trang chính
            # return render(request, "admin_page/home.html")
            messages.success(request, "Bạn đã đăng nhập thành công.")
            return redirect(reverse('home'))
            # return redirect('home')
        else:
            form.add_error(None, 'Vui lòng điền đầy đủ thông tin')
    else:
        form = CreateFormRegister()
        
    return render(request, "register.html", context={"form": form})

def is_super_or_staff(username):
    try:
        user = User.objects.get(username=username)
        return user.is_superuser or user.is_staff
    except User.DoesNotExist:
        return False

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None and is_super_or_staff(username):
                auth_login(request, user)
                return redirect(reverse('admin:index'))
            elif user is not None and not is_super_or_staff(username):
                request.session['user_name'] = user.username
                messages.success(request, "Bạn đã đăng nhập thành công.")
                # return HttpResponseRedirect(reverse('home') + '?username=' + user.username)
                return redirect(reverse('home'))
                # return render(request, "admin_page/home.html")
          
    else:        
        form = AuthenticationForm()

    return render(request, "login.html", context={"form":form})

def logout(request):
    if "user_name" in request.session:
        del request.session["user_name"]
    # products = Product.objects.all()

    return redirect(reverse('home'))
    # return render(request,'home.html', {'products': products})


def home(request):
    products = Product.objects.all()
   
    username = request.session.get("user_name", None)
    return render(request, 'home.html', {'products': products, 'user_name': username})

def filter_product(request,brand_id):
    products = Product.objects.filter(category__name_category=brand_id)
    return render(request,'filter_product.html', {'products': products})


def search_product(request):
    query = request.GET.get('q')
    if query:
        product_names = Product.objects.filter(name__icontains=query)           
    else:
        product_names = Product.objects.all()
    return render(request, 'search_product.html', {'product_names': product_names}) 



