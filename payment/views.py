from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect

from .models import Payment


def verify_payment(request, ref: str):
    payment: Payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successful!")
        return redirect('orders:order-placed')
    else:
        messages.error(request, "Verification Failed!")
        return redirect('orders:order-placed')
        # return render(request, 'orders/orderplaced.html', {'billing_status': verified})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
