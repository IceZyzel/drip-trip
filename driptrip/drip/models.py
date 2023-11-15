from django.db import models
from django import forms
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

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
    ('Ethical and Sustainable Fashion', 'Ethical and Sustainable Fashion'),
    ('Costumes and Cosplay', 'Costumes and Cosplay'),
    ('Designer Clothing', 'Designer Clothing'),
    )

class User (User):
    class Meta:
        proxy = True

class UserCourier (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Product (models.Model):
    userclient = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=64)
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
    userclient = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])
    date = models.DateField()

class Order (models.Model):
    userclient = models.ForeignKey(User,on_delete=models.CASCADE)
    usercourier = models.ForeignKey(UserCourier,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=12)
    adress = models.CharField(max_length=64)
    date = models.DateField()
    status = models.CharField(max_length=64)
    

class OrderProduct (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
