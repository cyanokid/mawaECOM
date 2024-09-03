from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from member.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product
import datetime


# Create your views here.
def show_orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get order 
        order = Order.objects.get(id=pk)
        # Get order items
        items = OrderItem.objects.filter(order=pk)

        # Marking shipping status
        if request.POST:
            # Get the status from posted form
            status = request.POST['shipping_status']

            # kalau value true/nak button shipped
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=True)
             # kalau value false/nak button not shipped
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)

            messages.success(request, "Shipping Status Updated.")
            return redirect('home')

        return render(request, 'payment/show_orders.html',{
            "order" : order,
            "items" : items,
        })
    else:
        messages.success(request, "Access Denied.")
        return redirect('home')
    
def shipped_dash(request):
    #must be loggedin and the admin
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the shipped order
        orders = Order.objects.filter(shipped=True)

        # Marking shipping status
        if request.POST:
            # Get the status from posted form
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # Update Order
            order.update(shipped=False)
            # redirect
            messages.success(request, "Shipping Status Updated.")
            return redirect('home')

        return render(request, 'payment/shipped_dash.html',{
            "orders" : orders,
        })
    else:
        messages.success(request, "Access Denied.")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the unshipped order
        orders = Order.objects.filter(shipped=False)

        # Marking shipping status
        if request.POST:
            # Get the status from posted form
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # Grab date and time 
            now = datetime.datetime.now()
            # Update Order
            order.update(shipped=True, date_shipped=now)
            # redirect
            messages.success(request, "Shipping Status Updated.")
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html',{
            "orders" : orders, 
        })
    else:
        messages.success(request, "You Have No Access To This Page")
        return redirect('home')
    

def process_order(request):
    
    if request.POST:
         # Get the cart
        cart = Cart(request)

        cart_products =  cart.get_prods #call the function we create 
        quantities= cart.get_quants
        totals = cart.cart_total()
        # Get the billing info from previous page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        # print(my_shipping)


        ## Create Shipping Address from sessions

        #{'csrfmiddlewaretoken': 'PqFYyHMCuOacrPIHEa2JfFqOnIfkTKIIMRPHUDvbNvWJYjNcXPCtdbtU4PDijEn5', 'shipping_full_name': 'asdada', 
        #'shipping_email': 'asda@gmail.com', 'shipping_address1': 'adaa', 'shipping_address2': '', 'shipping_state': 'asdas',
        # 'shipping_city': 'dasa', 'shipping_zipcode': 'dasas', 'shipping_country': 'dasdas'}
        # shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        # print(shipping_address)

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        amount_paid = totals

        # Create an Order
        # Here user and guest both can do order
        if request.user.is_authenticated:
            # Log in
            user = request.user

            # Create order/ fill in the model from form that we create
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add order item

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            # Do loops because there are possibly multiple product
            for product in cart_products():
                # Get the prodcut ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save() 

            # Delete our cart
            #loop tru session key
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete cart from database (old_cart_field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart_field)
            current_user.update(old_cart="")



            messages.success(request, "Order Placed!")
            return redirect('home')

        else:
            # Not Log in
            # Create order/ fill in the model from form that we create
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order item

            # Get the order ID
            order_id = create_order.pk

            # Get product Info
            # Do loops because there are possibly multiple product
            for product in cart_products():
                # Get the prodcut ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()  

            # Delete our cart
            #loop tru session key
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key] 

            messages.success(request, "Order Placed!")
            return redirect('home')


    else:
        messages.success(request, "Access Denied.")
        return redirect('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html',{

    })

def billing_info(request):
    # safety reason, hanya yang post request/tekan button yang boleh access
    if request.POST:
        # Get the cart
        cart = Cart(request)

        cart_products =  cart.get_prods #call the function we create 
        quantities= cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        # Can be a reference
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is logged in
        if request.user.is_authenticated:
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{
            "cart_products" : cart_products,
            "quantities" : quantities,
            "totals" : totals,
            "shipping_info" : request.POST,   #pass the posted shipping form
            "billing_form" : billing_form,
        })
        else:
            # Get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{
            "cart_products" : cart_products,
            "quantities" : quantities,
            "totals" : totals,
            "shipping_info" : request.POST,   #pass the posted shipping form
            "billing_form" : billing_form,
        })

        shipping_form = request.POST

        return render(request, 'payment/billing_info.html',{
        "cart_products" : cart_products,
        "quantities" : quantities,
        "totals" : totals,
        "shipping_form" : shipping_form,
        })
    else:
        messages.success(request, "Access Denied.")
        return redirect('home')

def checkout(request):
    # Get the cart
    cart = Cart(request)

    cart_products =  cart.get_prods #call the function we create 
    quantities= cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as log in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',{
        "cart_products" : cart_products,
        "quantities" : quantities,
        "totals" : totals,
        "shipping_form" : shipping_form,
    })
    else:
        # Check out as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',{
        "cart_products" : cart_products,
        "quantities" : quantities,
        "totals" : totals,
        "shipping_form" : shipping_form,
    })

