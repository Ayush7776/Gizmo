from django.shortcuts import render
from .models import Product,Contact
# Create your views here.
from django.http import HttpResponse

def index(request):
    products=Product.objects.all()
    return render(request,'shop/index.html',{'products':products})

def about(request):
    return render(request,'shop/about.html')

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

def tracker(request):
    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')

def productView(request,id):
    product=Product.objects.get(id=id)
    return render(request,'shop/productView.html',{'product':product})

def checkout(request):
    return render(request,'shop/checkout.html')