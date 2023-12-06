from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .models import Payment


def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successful!")
        return redirect('orders:order-placed')
    else:
        messages.error(request, "Verification Failed!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    