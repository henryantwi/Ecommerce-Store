from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from store.models import Product


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=100)
    country = models.CharField(max_length=250, default='Ghana')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)

    # Date the order was placed
    date_ordered = models.DateTimeField(default=timezone.now)

    # Tracking system for the order
    ORDER_STATUS_CHOICES = (
        (1, 'Waiting for confirmation'),
        (2, 'Order confirmed'),
        (3, 'Shipped'),
        (4, 'Out for delivery'),
        (5, 'Delivered'),
        (6, 'Unsuccessful delivery')
    )
    estimated_delivery_date = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)

    @staticmethod
    @receiver(post_save, sender='orders.Order')
    def update_related_order_items_status(sender, instance, **kwargs):
        # Check if the status of the Order has changed or if it's a new instance
        update_fields = kwargs.get('update_fields')
        if update_fields is not None and 'status' in update_fields or kwargs.get('created', False):
            related_order_items = OrderItem.objects.filter(order=instance)
            if related_order_items.exists():
                related_order_items.update(status=instance.status)

    def get_billing_status(self):
        try:
            from payment.models import Payment
            payment = self.payments.get(order=self)
            return payment.billing_status
        except Payment.DoesNotExist:
            return False

    def __str__(self):
        paid = self.get_billing_status()
        payment_successful = "Paid" if paid else "Issue with Payment"
        return f"Order #{self.pk}  [{payment_successful}]"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order #{self.order.pk} - {self.product.title}"


class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Order.ORDER_STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.title}"
