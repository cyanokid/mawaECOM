
## TO CREATE SESSION (TO KEEP TRACK USER ACTIVITIES)
## TO CREATE FUNCTIONS 

from store.models import Product
from member.models import Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get request
        self.request = request

        # get the current session key if it exist
        cart = self.session.get('session_key')

        # if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
 
        # Make sure the cart is available on all pages of site
        self.cart = cart

    # add function (used in views)
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # Deal with logged in user
        # make sure the user request is logged in
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'3':1, '2':4} to {"3":1, "2":4} double quotation
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model(but using update sebab dia dah difilter)
            current_user.update(old_cart=carty)

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # Deal with logged in user
        # make sure the user request is logged in
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'3':1, '2':4} to {"3":1, "2":4} double quotation
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model(but using update sebab dia dah difilter)
            current_user.update(old_cart=str(carty))


    # function to calculate total
    def cart_total(self):
        #get product IDS
        product_ids = self.cart.keys()
        #lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        #get quantities
        quantities = self.cart
        #start counting from 0
        total = 0

        for key, value in quantities.items():
            #convert key string into int to make calculations
            key = int(key) 
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.is_sale * value)
                    else:
                        total = total + (product.price * value)

        return total

    def __len__(self):
        # cart from context processor
        return len(self.cart)


    def get_prods(self):

        #get id from cart
        product_ids = self.cart.keys()

        #look id to look up the products in db model
        products = Product.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get cart
        ourcart = self.cart
        #Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        # make sure the user request is logged in
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'3':1, '2':4} to {"3":1, "2":4} double quotation
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model(but using update sebab dia dah difilter)
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        # make sure the user request is logged in
        if self.request.user.is_authenticated:
            # Get the current user
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #{'3':1, '2':4} to {"3":1, "2":4} double quotation
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to Profile Model(but using update sebab dia dah difilter)
            current_user.update(old_cart=str(carty))


    