from django.contrib import admin
from produit.models import *

# Register your models here.

admin.site.register(Produit)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(WishlistItem)
admin.site.register(Wishlist)
admin.site.register(Coupon)