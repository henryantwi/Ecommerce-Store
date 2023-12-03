from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
        
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category            = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)
    title               = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='Other Brand')
    description         = models.TextField()
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    past_price          = models.DecimalField(max_digits=10, decimal_places=2)
    image               = models.ImageField(upload_to='images/', default='images/default.jpg')
    additional_image_1  = models.ImageField(upload_to='images/', blank=True, null=True)
    additional_image_2  = models.ImageField(upload_to='images/', blank=True, null=True)
    additional_image_3  = models.ImageField(upload_to='images/', blank=True, null=True)
    slug                = models.SlugField(max_length=255)
    in_stock            = models.BooleanField(default=True)
    is_active           = models.BooleanField(default=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    objects             = models.Manager()
    products            = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)  # descending order

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def rating_count(self, star):
        return self.reviews.filter(rating=star).count()
    
    def total_reviews(self):
        return self.reviews.count()
    
    def average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    def __str__(self):
        return self.title
    
    
class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, default='General')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.product.title[:40]} - {self.user.full_name.split(' ')[0]}"
