from django.conf import settings
from shop.models import Book
from decimal import Decimal

class Cart:
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
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in = book_ids)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]['book'] = book
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # creating a method for getting the no of items in the cart
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # now save the cart sessioin
    def save(self):
        self.session.modified = True
    
    '''
    add method for adding items to cart
    We only need book_id and quantity for adding items to cart
    We want to increase quantity for adding same book
    '''
    def add(self, book, quantity=1, overrides_quantity=False):
        book_id = str(book.id) # id in cart session are mostly strings 
        if str(book_id) not in self.cart:
            self.cart[book_id] = {
                "quantity": 0,
                "price": str(book.price)
            }
        if overrides_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
            self.save()
    # add a remove method to remove the book
    def remove(self, book_id):
        book_id = str(book_id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()
            
        
    # a delete cart session method
    def delete_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())