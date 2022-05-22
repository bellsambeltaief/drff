from rest_framework import  serializers
from .models import *

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class AddProductToCartSerilizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item','quantity']

class RemoveProductToCartSerilizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item']


class CreateOrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']      


class AddProductToWishlistSerilizer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['item','quantity']


class CreateWishlistSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id']  