from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phone=models.CharField(max_length=20)
    
class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    is_active=models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",default="default.jpg")
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    stock=models.IntegerField(default=1)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    @property
    def cart_item(self):
        # qs=BasketItem.object.filter(basket=self)   #---> If there is no related name use this ORM query
        return self.cartitem.all()
    
    @property
    def cart_item_quantity(self):
        qs=self.cart_item
        return qs.count
    
    @property
    def sub_totel(self):
        basket_item=self.cart_item
        total_sum=0
        if basket_item:
            total_sum=sum([p.total for p in basket_item ])
        return total_sum
    
class BasketItem(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)  
    
    @property
    def total(self):
        return self.quantity*self.product.price 


class Complaints(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='complaint',blank=True)
    text=models.CharField(max_length=200,blank=True,null=True)
    description=models.CharField(max_length=200,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    status_choice=[
        ('inprogress','Inprogress'),
        ('rejected','Rejected'),
        ('accepted','Accepted'),
        ('delivery','Delivery')
    ]
    order_status=models.CharField(max_length=200,choices=status_choice,default='inprogress')
    total=models.CharField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    

def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)
    
post_save.connect(create_basket,sender=User)