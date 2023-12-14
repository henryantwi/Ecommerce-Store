from django.contrib import admin

from .models import OrderItem, Order, OrderTracking

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderTracking)
