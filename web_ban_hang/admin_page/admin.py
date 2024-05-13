from django.contrib import admin
from .models import *
from django.utils.html import mark_safe

class Account_Admin(admin.ModelAdmin):
    list_display = ["id", "user_name", "email", "role", "password"]
    search_fields = ["user_name", "email"]
    list_filter = ["user_name"]

class Detail_Account_Admin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "account_id"]
 
class Category_Admin(admin.ModelAdmin):
    list_display = ["id", "name_category"]

class Product_Admin(admin.ModelAdmin):
    list_display = ["category", "name", "price", "avatar"]  
    search_fields = ["name"]
    list_filter = ["category"]
    readonly_fields = ["avatar"]
    
    def avatar(self, product):
        return mark_safe("<img src='/static/{img_url}' alt ='{alt}' width='120px'/>".format(img_url=product.image.name, alt=product.image.name))

admin.site.register(Account, Account_Admin)
admin.site.register(Detail_Account, Detail_Account_Admin)
admin.site.register(Category, Category_Admin)
admin.site.register(Product, Product_Admin)
