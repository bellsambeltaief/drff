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



class GetProductRatingSerilizer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField("get_product_rating_stars")
    user = serializers.SerializerMethodField("get_product_rating_user")
    product = serializers.SerializerMethodField("get_product_name")

    def get_product_rating_stars(self, obj):
        return f"{obj.rating} stars" 

    def get_product_rating_user(self, obj):
        return obj.user.email

    def get_product_name(self, obj):
        return obj.product.prod_name
        
    class Meta:
        model = Rating
        exclude = ['id']