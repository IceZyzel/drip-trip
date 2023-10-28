from django.db import models
from django import forms
from django.core.validators import MaxValueValidator

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
    brand = models.CharField(max_length=64)
    description = models.TextField(max_length=250)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    category = models.TextField(max_length=250)

class Size(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    count = models.PositiveBigIntegerField()

class Review (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
class Order (models.Model):
    user_buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    user_courier = models.ForeignKey(User,on_delete=models.CASCADE)
    cartproduct = models.ForeignKey(CartProduct,on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    status = models.CharField(max_length=64)

class UserProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class PhotoProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photolink = models.CharField(max_length=100)