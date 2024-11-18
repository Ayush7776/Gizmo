from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category= models.CharField(max_length=50, default="")
    sub_category= models.CharField(max_length=50, default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image= models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name
    
    def get_total_price(self):
        return self.product.price * self.quantity

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product}"

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    name=models.CharField(max_length=150,default="")
    email=models.EmailField(max_length=50,default="")
    phone=models.CharField(max_length=20,default="")
    address=models.CharField(max_length=500,default="")
    paid=models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - Total: ${self.total_price}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} of {self.product.product_name}"

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=70)
    desc = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name