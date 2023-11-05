from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserClient)
admin.site.register(UserCourier)
admin.site.register(UserAdmin)
admin.site.register(Product)
admin.site.register(PhotoProduct)
admin.site.register(Size)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderProduct)
