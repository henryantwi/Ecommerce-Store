from django.contrib import admin

from .models import OrderItem, Payment

admin.site.register(Payment)
admin.site.register(OrderItem)
