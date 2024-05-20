from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home , name='home'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path('search/', views.search_product, name='search_product'),
    path("logout/", views.logout, name="logout"),
    path("view_information/", views.view_information, name="view_information"),
    path("update_information/", views.update_information, name="update_information"),
    path("change_password/", views.change_password, name="change_password"),
    path('detail/', views.detail_product, name='detail_product'),
    path('<str:brand_id>/', views.filter_product, name='filter_product'),   
]