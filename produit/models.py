from pyexpat import model
from django.db import models
from accounts.models import User
import random


# Create your models here.


CATEGORY_CHOICES = (
    ('Shirt', 'Shirt'),
    ('Sport wear', 'Sport wear'),
    ('Outwear', 'Outwear'),
    ('Tech', 'Tecknology'),
    ('Camping', 'Camping'),
)
ORDER_STATUS = (
    ('Ordered', 'Ordered'),
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Received', 'Received'),
    ('Cancelled', 'Cancelled'),

)

class Produit(models.Model):
    vender = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=255,null=False, blank=False)
    price = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True,upload_to="product_images/")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prod_name


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Produit, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.prod_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=50,choices=ORDER_STATUS,null=True, blank=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email

    def generate_ref_code(self):
        ref_code = random.randint(111111, 999999)
        return ref_code


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total -= self.coupon.amount
        return total



class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code




class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Produit, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.prod_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(WishlistItem)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total