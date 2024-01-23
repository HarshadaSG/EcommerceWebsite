import random
from django.shortcuts import render,HttpResponse,redirect
from .models import Product,CartItem,Order
from django.db.models import Q
from. forms import CreateUserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages


# Create your views here.
def index(request):
    products = Product.objects.all()
    context ={}
    context['products']=products
    return render(request,"index.html",context)

def proDetail(request,pid):
    products = Product.objects.get(product_id=pid)
    context = {'products':products}
    return render(request,'productDetail.html',context)

def viewCart(request):
    if request.user.is_authenticated:
        allproducts=CartItem.objects.filter(user = request.user)
    else:
        return redirect("/login")
    context={}
    context['cart_items']=allproducts
    total_price=0
    for x in allproducts:
        total_price+= (x.product.price * x.quantity)
        print(total_price)
    context['total']=total_price
    length=len(allproducts)
    context['items']=length
    return render(request,"cart.html",context)

def add_cart(request,pid):
    products = Product.objects.get(product_id=pid)
    user = request.user if request.user.is_authenticated else None
    print(products)
    if user:
        cart_item,created = CartItem.objects.get_or_create(product=products,user = user)
        print(cart_item,created)
    else:
        return redirect("/login")
        #cart_item,created = CartItem.objects.get_or_create(products = products)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect("/viewCart") 

def removeCart(request,pid):
    cart = CartItem.objects.filter(product_id=pid)
    cart.delete()
    return redirect("/viewCart")
    
def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(price__icontains=query)
        )

    return render(request, 'index.html', {'products': products})

def all_products(request):
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})

def watches(request):
    Watches = Product.objects.filter(category='Watch')
    return render(request,'index.html',{'products':Watches})

def Mobile(request):
    Mobile = Product.objects.filter(category='Mobile')
    return render(request,'index.html',{'products':Mobile})

def Laptop(request):
    Laptop = Product.objects.filter(category='Laptop')
    return render(request,'index.html',{'products':Laptop})


def range(req):
    r1 = req.POST.get("min")
    r2 = req.POST.get("max")
    print(r1,r2)
    if r1 is not None and r2 is not None and r1 != "" and r2 != "":
        queryset = Product.objects.price__range(r1,r2)
        context = {'product' : queryset}
        return render (req,"index.html",context)
    else:
        queryset = Product.objects.all()
        context = {'products' : queryset}
        return redirect(req,"index.html",context)
               
def product_list_high_to_low(request):
    products = Product.objects.order_by('-price')
    return render(request, 'index.html', {'products': products})

def product_list_low_to_high(request):
    products = Product.objects.order_by('price')
    return render(request, 'index.html', {'products': products})


def updateqty(request,uval,pid):
    
    user = request.user
    c = CartItem.objects.filter(product_id = pid ,user = user)
    print(c)
    print(c[0])
    print(c[0].quantity)
    if uval == 1:
        a = c[0].quantity + 1
        c.update(quantity = a)
        print(c[0].quantity)
    else:
        a=c[0].quantity -1
        c.update(quantity = a)
        print(c[0].quantity)
    return redirect("/viewCart")



def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,("User Create Sucessfully"))
            return redirect("/login")
        else:
            messages.error(request,("incorrect Password Format"))
            return redirect("/register")
    context ={'form': form}
    return render(request,"register.html",context)


def login_user(req):
    if req.method =='POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,('You Have Been Logged In'))
            return redirect('/')
        else:
            messages.error(req,('incorrect Username Or Password'))
            return redirect('/login')
    else:
        return render(req,"login.html")

def user_logout(req):
    logout(req)
    messages.success(req, 'Log Out Successfully')  # Fix the typo here
    return redirect('/')

def viewOrder(req):
    c = CartItem.objects.filter(user=req.user)
    oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,product_id=x.product.product_id,user=req.user,quantity=x.quantity)
    orders=Order.objects.filter(user=req.user)
    context={}
    context['cart_items']= orders
    total_price=0
    for x in orders:
        total_price+= (x.product.price * x.quantity)
        print(total_price)
    context['total']=total_price
    length=len(orders)
    context['items']=length
    return render(req,"vieworder.html",context)
import razorpay
def makepayment(req):
    orders=Order.objects.filter(user=req.user)
    total_price=0
    for x in orders:
        total_price+= (x.product.price * x.quantity)
        oid= x.order_id
        print(oid)
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_p8frIxrMeZN3YF", "EhbzxqlOO0SUze1r5R7emUgX"))
    data={
    "amount": total_price*100,
    "currency": "INR",
    "receipt": "oid"
    }
    payment=client.order.create(data=data)
    context={}
    context['data']=payment
    context['amount']=payment["amount"]
    return render(req,"payment.html",context)
                    