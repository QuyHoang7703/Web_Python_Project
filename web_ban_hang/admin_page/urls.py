from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home , name='home'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path('search/', views.search_product, name='search_product'),
    path("logout/", views.logout, name="logout"),
    path("view_information/", views.view_information, name="view_information"),
    path("update_information/", views.update_information, name="update_information"),
    path("change_password/", views.change_password, name="change_password"),
     # URL reset password
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
  
    path('detail/', views.detail_product, name='detail_product'),
    path('cart/', views.cart, name='cart'),
    path('addcart/', views.addcart, name='addcart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('recalculate_cart_total/', views.recalculate_cart_total, name='recalculate_cart_total'),
    path('payment/', views.payment, name='payment'),
    path('<str:brand_id>/', views.filter_product, name='filter_product'),   
]