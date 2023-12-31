from os import truncate
from django.db import models
from django import forms
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unisex'),
    )

CATEGORY_CHOICES = (
    ('Shoes', 'Shoes'),
    ('Accessories', 'Accessories'),
    ('Activewear', 'Activewear'),
    ('Outerwear', 'Outerwear'),
    ('Formal Wear', 'Formal Wear'),
    ('Casual Wear', 'Casual Wear'),
    ('Underwear', 'Underwear'),
    ('Swimwear', 'Swimwear'),
    ('Vintage Clothing', 'Vintage Clothing'),
    ('Maternity Wear', 'Maternity Wear'),
    ('Sportswear', 'Sportswear'),
    ('Sleepwear', 'Sleepwear'),
    ('Workwear', 'Workwear'),

    )

class User (User):
    class Meta:
        proxy = True

class UserCourier (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Product (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.FloatField()
    brand = models.CharField(max_length=64)
    description = models.TextField(max_length=250)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

class PhotoProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photolink = models.ImageField(upload_to='products_photo/')

class Size (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    count = models.PositiveBigIntegerField()

class Review (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])
    date = models.DateField(default=timezone.now)

class Order (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    usercourier = models.ForeignKey(UserCourier,on_delete=models.CASCADE, null=True)
    adress = models.CharField(max_length=64)
    full_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=12) 
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=64)

class OrderProduct (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size_name = models.CharField(max_length=12)
