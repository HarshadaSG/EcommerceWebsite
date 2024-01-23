from django.db import models
from django.contrib.auth.models import User

#Custom Manager
class CustomManager(models.Manager):
    def get_price_range(self,r1,r2):
        return self.filter(price__range = (r1,r2))

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length = 55)
    desc = models.CharField(max_length=255)
    type = (("Mobile","mobile"),("Watch","watch"),("Laptop","laptop"))
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="pics")
    
    prod = CustomManager() #custom manager
    objects = models.Manager() #default manager
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)

class Order(models.Model):
    order_id=models.IntegerField()
    product = models.ForeignKey(Product,on_delete = models.CASCADE)  
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1)
    is_completed=models.BooleanField(default = False)
    

    