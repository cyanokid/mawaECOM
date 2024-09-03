from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#for register
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .forms import RegisterUserForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Profile
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


# Create your views here.
def update_info(request):
    if request.user.is_authenticated:
        # Get the current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get the current user in shipping
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get user Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, ("Your Info is Updated!"))
            return redirect('home')

        return render(request, 'authenticate/update_info.html',{
            "form" : form,
            "shipping_form" : shipping_form,
    })

    else:
        messages.success(request, ("You Must Be Logged In To View This Page."))
        return redirect('home')  
    

def update_password(request):
    if request.user.is_authenticated:
        # Get the current user
        current_user = request.user
        #if post
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Your Password is Updated."))
                login(request, current_user) 
                return redirect('home')  

            else:
                #pass django authentication error
                for error in list(form.errors.values()):
                    messages.error(request, error) 
                    return redirect('update_password') 
                
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'authenticate/update_password.html',{
                "form" : form,
            })
    else:
        messages.success(request, ("You Must Be Logged In To View This Page."))
        return redirect('home')     

def update_user(request):
    if request.user.is_authenticated:
        # Get the current user
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ("Your Profile is Updated!"))
            return redirect('home')

        return render(request, 'authenticate/update_user.html',{
        "user_form" : user_form,
    })

    else:
        messages.success(request, ("You Must Be Logged In To View This Page."))
        return redirect('home') 


def login_user(request):
    if request.method == "POST":
        #get the username and password input
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Do some shopping cart stuff
            # get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                #convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                #add loaded cart dictionary to our session
                #get the cart
                cart = Cart(request)
                #loop through the cart and add items from database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
           
            # Redirect to a success page.
            messages.success(request, ("You are log in successfully."))
            return redirect('home')

        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There is an Error. Please Try to Login Again."))
            return redirect('login')
    else:

        return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    # Redirect to a success page.
    messages.success(request, ("You were Logged Out."))
    return redirect('home')

def register_user(request):
    form = RegisterUserForm()
    if request.method == "POST":
        #take the input of form
        form = RegisterUserForm(request.POST)
        #check the validity
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] 
            #login user
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You Successfully Register to mawECOM - Please Complete Your Profile Info."))
            return redirect('update_info')
        
        else:
            messages.success(request, ("You Information is Not Valid. Register Again "))
            return redirect('register')

    else:
        return render(request, 'authenticate/register.html',{
            "form" : form,
        })