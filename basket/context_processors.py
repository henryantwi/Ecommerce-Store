from .basket import Basket

def basket(request):
    context = {
        'basket': Basket(request)
    }
    return context  