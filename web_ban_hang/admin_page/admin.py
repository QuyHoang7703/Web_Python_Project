from django.contrib import admin
from .models import *
from django.utils.html import mark_safe

admin.site.site_header = "Admin Page"
# class User_Admin(admin.ModelAdmin):
#     list_display = ["id", "get_username", "get_email"]
#     # search_fields = ["username", "email"]
#     # list_filter = ["role"]

#     def get_username(self, obj):
#         return obj.username
#     get_username.short_description = 'Username'

#     def get_email(self, obj):
#         return obj.email
#     get_email.short_description = 'Email'

    # def get_role(self, obj):
    #     return obj.get_role_display()
    # get_role.short_description = 'Role'

class Customer_Admin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "user"]
 
class Category_Admin(admin.ModelAdmin):
    list_display = ["id", "name_category"]

class Product_Admin(admin.ModelAdmin):
    list_display = ["id", "category", "name", "price", "avatar"]  
    search_fields = ["name"]
    list_filter = ["category"]
    readonly_fields = ["avatar"]
    
    def avatar(self, product):
        return mark_safe("<img src='/static/{img_url}' alt ='{alt}' width='110px'/>".format(img_url=product.image.name, alt=product.image.name))

class Size_Admin(admin.ModelAdmin):
    list_display = ["id", "name"]

class ProductSize_Admin(admin.ModelAdmin):
    list_display = ["get_name_product", "get_size_product", "quantity", "avatar"]
    readonly_fields= ["avatar"]
    search_fields = ["product__name", "size__name"]
    list_filter = ["size__name"]
    def avatar(self, product_size):
        return mark_safe("<img src='/static/{img_url}' alt ='{alt}' width='110px'/>".format(img_url=product_size.product.image.name, alt=product_size.product.image.name))


# admin.site.register(User, User_Admin)
admin.site.register(Customer, Customer_Admin)
admin.site.register(Category, Category_Admin)
admin.site.register(Product, Product_Admin)
admin.site.register(Size, Size_Admin)
admin.site.register(ProductSize, ProductSize_Admin)