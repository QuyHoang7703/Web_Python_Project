























from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=100, null=False, blank=False)

    def get_email(self):
        return self.user.email
    get_email.short_description = "Email"
class Category(models.Model):
    name_category = models.CharField(max_length=100, null=False, unique=True, blank=False)
    def __str__(self):
        return self.name_category

class Product(models.Model):
    category = models.ForeignKey(Category, models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField()
    image = models.ImageField(upload_to="products", default=None)

class Size(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False) 

class ProductSize(models.Model):
    product = models.ForeignKey(Product, models.SET_NULL, null=True)
    size = models.ForeignKey(Size, models.SET_NULL, null=True)
    quantity = models.IntegerField()
    class Meta:
        unique_together =('product', 'size')
    
    def get_name_product(self):
        return self.product.name
    
    def get_size_product(self):
        return self.size.name

    def get_img_product(self):
        return self.product.image

    def get_price_product(self):
        return self.product.price
    
    get_name_product.short_description = "Product Name"
    get_size_product.short_description = "Size"
    get_img_product.short_description = "Image"
    # get_price_product.short_description = "Price"
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Tham chiếu đến model Customer
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=30, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False)
    
    def get_total_price(self):
        return self.price
    
    get_total_price.short_description = "Total Price"