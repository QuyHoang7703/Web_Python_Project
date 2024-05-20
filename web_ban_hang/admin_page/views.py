from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib import messages
from .forms import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
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
            request.session['user_name'] = user.username
            messages.success(request, "Bạn đã đăng nhập thành công.")
            return redirect(reverse('home'), {"username": username})
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
    return render(request, "login.html")
    # return render(request, "login.html", context={"form":form})
   

def logout(request):
    if "user_name" in request.session:
        del request.session["user_name"]

    return redirect(reverse('home'))



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

@login_required
def view_information(request):
    user_name = request.GET.get("user_name", None)
    # print("Username: ", user_name)
    if user_name:
        print("Username: ", user_name)
        user= User.objects.get(username=user_name)
        customer = Customer.objects.get(user=user)
        if user and customer:
            name = customer.name
            address = customer.address
            phone = customer.phone
            email = user.email
            print(name, address, phone, email)
            context={
                "user_name": user_name,
                "name": name,
                "address" : address,
                "phone": phone,
                "email": email
            }
        return render(request, "view_information.html", context=context)  
    else:
        return HttpResponse("Không tìm thấy tên người dùng trong yêu cầu.")

def update_information(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        email = request.POST.get("email")
        print(username, name, address)
        
        user= User.objects.get(username= username)
        customer = Customer.objects.get(user=user)
        customer.name = name
        customer.address = address
        customer.phone = phone
        user.email = email
        customer.save()
        user.save()
        
        # Redirect to a success page or any other page
        return redirect(reverse("home"))  # Replace 'success_page_url' with the URL of your success page
        
    return HttpResponse("Không tìm thấy người dùng hoặc thông tin khách hàng tương ứng blo.")

def change_password(request):
    if request.method == "GET":
        user_name = request.GET.get("user_name")
        context = {"user_name": user_name}
        return render(request, "change_password.html", context=context)
    
    if request.method == 'POST':
        user_name = request.POST.get("username")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        # Kiểm tra xem tất cả các trường thông tin đã được điền đầy đủ
        if not (old_password and new_password and confirm_password):
            messages.error(request, "Vui lòng điền đầy đủ thông tin")
            return redirect(reverse('change_password') + f'?user_name={user_name}')

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            messages.error(request, "Tài khoản không tồn tại")
            return redirect(reverse('change_password'))

        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Mật khẩu đã được thay đổi thành công!")
                return redirect(reverse("home"))
            else:
                messages.error(request, "Mật khẩu mới và xác nhận mật khẩu không trùng khớp")
        else:
            messages.error(request, "Mật khẩu hiện tại không chính xác")
        
        return redirect(reverse('change_password') + f'?user_name={user_name}')
    


def detail_product(request):
    if 'detail' in request.GET:
        product_id = request.GET['detail']
        product_sizes = ProductSize.objects.filter(product_id=product_id) 
        return render(request, 'detail_product.html', {'product_sizes': product_sizes})
    