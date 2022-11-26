from django.conf import settings
from shop.models import Book

class Cart(object):
    # create a cosnstructor for cart class
    def __init__(self, request):
        # set a session for cart
        self.session = request.session
        # create a cart session object
        cart = self.session.get(settings.CART_SESSION_ID)
        # check cart exists or not. If not then create an empty instance
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    # creating a iteration method for displaying the books in the cart
    def __iter__(self):
        for pk in self.cart.keys():
            self.cart[str(pk)]["product"] = Book.objects.get(pk=pk)

    # creating a method for getting the no of items in the cart
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # now save the cart sessioin
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    '''
    add method for adding items to cart
    We only need product_id and quantity for adding items to cart
    We want to increase quantity for adding same product
    '''
    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id) # id in cart session are mostly strings 
        if str(product_id) not in self.cart:
            self.cart[product_id] = {
                "quantity": 1,
                "id": product_id,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product_id)
        
        self.save()
    # add a remove method to remove the product
    def remove(self, product_id):
        if self.cart[product_id]:
            self.save()
        
    # a delete cart session method
    def delete_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        