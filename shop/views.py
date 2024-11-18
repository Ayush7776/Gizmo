from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Contact,CartItem,Order,OrderItem
from django.conf import settings
from django.http import HttpResponse

def index(request):
    products=Product.objects.all()
    cart_items = CartItem.objects.all()
    return render(request,'shop/index.html',{'products':products,'cart_items':cart_items})

def cart_detail(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('index')

def update_cart(request, product_id, action):
    cart_item = get_object_or_404(CartItem, product_id=product_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity = max(1, cart_item.quantity - 1)
    cart_item.save()
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id)
    cart_item.delete()
    return redirect('cart_detail')



def checkout(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.all()
        if not cart_items:
            return HttpResponse("Your cart is empty")
        
        total_price = sum(item.get_total_price() for item in cart_items)
        name=request.POST['fname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']+" "+request.POST['pincode']
        order=Order.objects.create(name=name,email=email,phone=phone,address=address,total_price=total_price,paid=True)

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        
        cart_items.delete()

        return render(request, 'shop/checkout_success.html', {'order': order})
    return render(request, 'shop/checkout.html')


def order_list(request):
    orders = Order.objects.filter(paid=True)
    return render(request, 'shop/order_list.html', {'orders': orders})


def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        return render(request,'shop/contact.html',{'massage':"We Will Contact You Imegetly","color":"danger"})
    return render(request,'shop/contact.html')


def productView(request,id):
    product=Product.objects.get(id=id)
    return render(request,'shop/productView.html',{'product':product})

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')
def about(request):
    return render(request,'shop/about.html')