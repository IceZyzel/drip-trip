from django.db import models
from django import forms
from django.core.validators import MaxValueValidator

# Create your models here.
ROLE_CHOICES = (
    ('Purchaser'),
    ('Salesperson'),
    ('Admin'),
    ('Courier'),
    )
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unisex'),
    )
class Size(models.Model):
    text= models.CharField(max_length=64)

class SizeProduct(models.Model):
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    role = models.CharField(max_length=11 , choices=ROLE_CHOICES)
    
class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=64)
    count = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    description = models.TextField(max_length=250)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    category = models.TextField(max_length=250)

class Review (models.Model):
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])

class Order (models.Model):
    address = models.CharField(max_length=64)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

class UserProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
 