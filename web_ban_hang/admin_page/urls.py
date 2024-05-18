from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home , name='home'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path('search/', views.search_product, name='search_product'),
    path('<str:brand_id>/', views.filter_product, name='filter_product'),
    path("logout/", views.logout, name="logout"),
    
]