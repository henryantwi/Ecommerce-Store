from urllib import response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    context = {
        'basket': basket,
    }
    return render(request, 'basket/summary.html', context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        # basket_total = 'GH₵ {:,.2f}'.format(basket.get_total_price())
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_subtotal, 'total': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        basketqty = basket.__len__()
        # basket_total = 'GH₵ {:,.2f}'.format(basket.get_total_price())
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_subtotal, 'total': basket_total})
        return response
