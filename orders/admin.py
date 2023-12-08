from django.contrib import admin

from .models import OrderItem, Order, OrderTracking, ProductReview

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderTracking)
admin.site.register(ProductReview)
