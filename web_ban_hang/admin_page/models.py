from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.forms import UserCreationForm


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Account(models.Model):
    user_name = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)
    role = models.IntegerField(null=False)
    # avatar = models.ImageField(upload_to='uploads/%Y/%m')
    # def __str__(self):
    #     return self.user_name + " " + self.password

class Detail_Account(models.Model):
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False) 
    phone = models.CharField(max_length=100, null=False)
    # sex = models.BooleanField()
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

class Category(models.Model):
    name_category = models.CharField(max_length=50, null=False, unique=True, blank=False)
    def __str__(self):
        return self.name_category

class Product(models.Model):
    category = models.ForeignKey(Category, models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField()
    image = models.ImageField(upload_to="products", default=None)