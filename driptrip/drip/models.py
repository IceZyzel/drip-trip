from django.db import models
from django import forms
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unisex'),
    )

class User (User):
    class Meta:
        proxy = True
    
class UserClient (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class UserCourier (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class UserAdmin (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Product (models.Model):
    userclient = models.ForeignKey(UserClient,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    description = models.TextField(max_length=250)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    category = models.TextField(max_length=250)
    date = models.DateField()

class PhotoProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photolink = models.CharField(max_length=100)

class Size (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    count = models.PositiveBigIntegerField()

class Review (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    userclient = models.ForeignKey(UserClient,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    rate = models.IntegerField(validators=[MaxValueValidator(5)])
    date = models.DateField()

class Order (models.Model):
    userclient = models.ForeignKey(UserClient,on_delete=models.CASCADE)
    usercourier = models.ForeignKey(UserCourier,on_delete=models.CASCADE)
    adress = models.CharField(max_length=64)
    date = models.DateField()
    status = models.CharField(max_length=64)

class OrderProduct (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
