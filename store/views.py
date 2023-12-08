from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from basket.basket import Basket
from orders.models import OrderItem

from .models import Category, Product, ProductReview


def calculate_percentage(count, total_count):
    return (count * 100) / total_count if total_count != 0 else 0

def product_all(request):
    """Home Page of the site displaying all products"""
    # products = Product.objects.all()
    products = Product.objects.filter(in_stock=True).order_by('?')
    context = {
        'products': products,
    }
    return render(request, 'store/home.html', context)


def product_detail(request, slug):
    basket = Basket(request)
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    product_qty = basket.get_product_qty(product.id)
    reviews = product.reviews.all().order_by('-rating')
    total_count = product.total_reviews()
    # total_count = sum(product.ratings_count.values())
    
    percentage_1_star  = calculate_percentage(product.rating_count(1), total_count)
    percentage_2_stars = calculate_percentage(product.rating_count(2), total_count)
    percentage_3_stars = calculate_percentage(product.rating_count(3), total_count)
    percentage_4_stars = calculate_percentage(product.rating_count(4), total_count)
    percentage_5_stars = calculate_percentage(product.rating_count(5), total_count)
    
    ratings_count = {
        '5_stars': product.rating_count(5),
        '4_stars': product.rating_count(4),
        '3_stars': product.rating_count(3),
        '2_stars': product.rating_count(2),
        '1_star': product.rating_count(1),
    }
    
    rating_percentages = {
        'one': percentage_1_star, 
        'two': percentage_2_stars,
        'three': percentage_3_stars,
        'four': percentage_4_stars,
        'five': percentage_5_stars,
    }
    

    total_purchases = OrderItem.objects.filter(
        # order__billing_status=True,
        product=product,
    ).count()

    context = {
        'product': product,
        'product_qty': product_qty,  
        'reviews': reviews,
        'ratings_count': ratings_count,
        'rating_percentages':rating_percentages,
        'total_purchases': total_purchases,
    }
    return render(request, 'store/products/single.html', context)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/products/category.html', context)


def search_products(request):
    query = request.GET.get('q')

    if query:
        # Filter products by name, category, brand, and in_stock=True
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__icontains=query),
            in_stock=True
        ).order_by('?')
    else:
        # Retrieve all in-stock products
        products = Product.objects.filter(in_stock=True).order_by('?')
        # products = Product.objects.filter(in_stock=True)

    return render(request, 'store/products/search_results.html', {'products': products, 'query': query})