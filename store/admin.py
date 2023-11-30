from django.contrib import admin

from .models import Category, Product, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'slug',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'price',
        'in_stock',
        'created',
        'updated',
    ]
    
    list_filter = [
        'in_stock',
        'is_active',
    ]
    
    list_editable = [
        'price',
        'in_stock',     
    ]

    prepopulated_fields = {
        'slug': ('title', )
    }
    
    
admin.site.register(ProductReview)