from django.shortcuts import render, redirect, get_object_or_404  
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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST

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

    
def cart(request):
    user_name = request.session.get('user_name')
    customer = get_object_or_404(Customer, user=User.objects.get(username=user_name))
    cart_items = Cart.objects.filter(customer=customer, status=False)

    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def addcart(request):
    if request.method == 'POST':
        # Lấy user_id từ session
        user_name = request.session.get('user_name')
        
        # Lấy hoặc tạo instance của Customer từ user_name
        customer, _ = Customer.objects.get_or_create(user=User.objects.get(username=user_name))
        
        if customer:
            product_id = request.POST.get('product_id')
            size_name = request.POST.get('size_id')
            quantity = int(request.POST.get('quantity', 1))

            product = get_object_or_404(Product, id=product_id)
            price = product.price * quantity

            # Tạo giỏ hàng chỉ khi có customer
            cart_item, created = Cart.objects.get_or_create(
                customer=customer,
                product=product,
                size=size_name,
                status = 0,
                defaults={'quantity': quantity, 'price': price}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.price += price
                cart_item.save()

    return redirect('home')

def checkout(request):
    # Xử lý logic thanh toán ở đây
    # Ví dụ: Tạo hóa đơn, xử lý thanh toán, vv.
    # Sau khi xử lý thành công, có thể chuyển hướng người dùng đến trang cảm ơn hoặc trang chính.
    messages.success(request, 'Thanh toán thành công!')
    return redirect('home')

# def payment(request):
#     if request.method == 'POST':
#         # Lấy user_name từ session
#         user_name = request.session.get('user_name')
        
#         # Lấy hoặc tạo instance của Customer từ user_name
#         customer, _ = Customer.objects.get_or_create(user=User.objects.get(username=user_name))
        
#         if customer:
#             # Lấy ra tất cả các mục trong giỏ hàng của khách hàng
#             cart_items = Cart.objects.filter(customer=customer, status=False)
            
#             # Đánh dấu các mục trong giỏ hàng là đã thanh toán
#             for item in cart_items:
#                 item.status = True
#                 item.save()
#                  # Lấy sản phẩm tương ứng của mục trong giỏ hàng
#                 # Lấy thông tin về sản phẩm kích thước tương ứng
#                 size_obj = Size.objects.get(name=item.size)

#                 product_size = ProductSize.objects.get(product=item.product, size=size_obj.id)

#                 # Trừ đi số lượng đã thanh toán để cập nhật số lượng tồn kho
#                 product_size.quantity -= item.quantity
#                 product_size.save()
#             return redirect('cart')
#     else:
#         # Xử lý khi không phải là phương thức POST
#         # Có thể cần xử lý báo lỗi hoặc chuyển hướng đến trang khác
#         pass

def remove_from_cart(request, cart_item_id):
    # Xác định sản phẩm cần xóa từ giỏ hàng
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    # Xóa sản phẩm khỏi giỏ hàng
    cart_item.delete()
    messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng.')
    return redirect('cart')  # Chuyển hướng người dùng đến trang giỏ hàng sau khi xóa

def recalculate_cart_total(request):
    if request.method == 'POST':
        # Tính toán lại tổng giá trị của giỏ hàng ở đây
        user_name = request.session.get('user_name')
        customer = get_object_or_404(Customer, user=User.objects.get(username=user_name))
        cart_items = Cart.objects.filter(customer=customer, status=False)

        total_price = sum(item.get_total_price() for item in cart_items)
        # Trả về tổng giá trị dưới dạng JSON
        return JsonResponse({'total_price': total_price})
    
def payment(request):
    if request.method == 'POST':
        user_name = request.session.get('user_name')
        customer, _ = Customer.objects.get_or_create(user=User.objects.get(username=user_name))
        
        if customer:
            cart_items = Cart.objects.filter(customer=customer, status=False)
            total_price = 0
            cart_item_ids = []

            for item in cart_items:
                total_price += item.get_total_price()
                cart_item_ids.append(str(item.id))
                
                # Cập nhật số lượng sản phẩm trong ProductSize
                size = Size.objects.get(name=item.size)
                product_size = ProductSize.objects.get(product=item.product, size=size)
                product_size.quantity -= item.quantity
                product_size.save()
                
                # Đánh dấu các mục trong giỏ hàng là đã thanh toán
                item.status = True
                item.save()
            
            # Tạo bản ghi hóa đơn
            cart_item_ids_str = ','.join(cart_item_ids)
            bill = Bill(user=customer.user, total_price=total_price, date=timezone.now(), cart_item_ids=cart_item_ids_str)
            bill.save()
            
            messages.success(request, 'Thanh toán thành công!')
            return redirect('home')
        else:
            messages.error(request, 'Khách hàng không tồn tại')
            return redirect('cart')
    else:
        messages.error(request, 'Yêu cầu không hợp lệ')
        return redirect('cart')