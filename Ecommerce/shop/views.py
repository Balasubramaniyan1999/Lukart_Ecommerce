from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request,'shop/index.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username = name,password = pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Loggedin Successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password! Try again...")
                return redirect('/login')
        return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully")
    return redirect('/')

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Regsitration Success you can login now !")
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})


def collections(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name = name,status=0)):
        products = Product.objects.filter(category__name = name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such Categories are found")
        return redirect('collections')
    

def product_details(request,cname,pname):
    if (Catagory.objects.filter(name=cname,status = 0)):
        if(Product.objects.filter(name=pname,status=0)):
            products= Product.objects.filter(name=pname,status= 0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No such Product was found")
            return redirect('collections')
    else:
        messages.error(request,"No such category was found")
        return redirect('collections')    
    
