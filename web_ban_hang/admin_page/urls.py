from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home , name='home'),
    path('search/', views.search_product, name='search_product'),
    path('<str:brand_id>/', views.filter_product, name='filter_product'),
    
]