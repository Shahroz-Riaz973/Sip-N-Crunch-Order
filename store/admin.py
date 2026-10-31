from django.contrib import admin
from .models import Category, Product, B2BClient, Order, OrderItem, SampleRequest

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(B2BClient)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SampleRequest)