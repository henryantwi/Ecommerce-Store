import secrets

from django.conf import settings
from django.db import models
from django.db.models import PositiveIntegerField

from .paystack import Paystack
from orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    billing_status = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user', null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f"[Payment: {self.amount}]-[Status: {self.billing_status}]"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount

    def verify_payment(self) -> bool:
        paystack: Paystack = Paystack()
        try:
            status, result = paystack.verify_payment(self.ref, self.amount)
            if status and result['amount'] == self.amount:
                self.billing_status = True
                self.save()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False
