from django.shortcuts import render, redirect 
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q      # to filter more than one 

# Create your views here.
def search(request):
    # Determine if they fill form
    if request.method == "POST":
        searched = request.POST['searched']

        # Query the product DB Model
        # searched = Product.objects.filter(name__icontains=searched)
        
        # Query for multiple DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #Test for null
        if not searched:
            messages.success(request, ("This Search Doesnt Exist."))
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {
                "searched" : searched,
            })

    else:
        return render(request, 'store/search.html', {})

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {
        "categories" : categories,    
    })

def category(request, foo):
    #replace hypens with spaces
    foo = foo.replace('-', ' ')
    
    try:
        #grab the category from url
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {
            "category" : category,
            "products" : products,
        })
    except:
        messages.success(request, ("This Category Doesnt Exist."))
        return redirect('home')

def product(request, pk):
    
    product = Product.objects.get(id=pk)

    return render(request, 'store/product.html',{
        "product": product,
    })

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {
        "products" : products, 
    })

def about(request):
    return render(request, 'store/about.html', {

    })

