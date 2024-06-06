from decimal import Decimal
from django.conf import settings
from store.models import Product


class Basket:
    """
    A base Basket class, providing some default behaviors
    that can be inherited or overrided, as necessary.
    """
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket
            
    def add(self, product, qty):
        """
        Adding and updating the users basket
        session data
        """
        product_id = str(product.id)

    
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': qty,
            }
            
        self.save()
        
    def __iter__(self):
        """
        Collect the product id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()
        
        for product in products:
            basket[str(product.id)]['product'] = product
            
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
        
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total
    
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)   
        
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
               
    def save(self):
        self.session.modified = True
        
    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        # del self.session['skey']
        self.save()
        
    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def get_product_qty(self, product_id):
        """
        Retrieve the quantity of a specific product in the basket
        """
        product_id = str(product_id)
        if product_id in self.basket:
            return self.basket[product_id]['qty']
        return 0  # Return 0 if the product is not in the basket
        