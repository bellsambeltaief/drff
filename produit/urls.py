from django.urls import path, include
from .api import *

urlpatterns = [
    path('create-product/',ProduitCreateApi.as_view()),
    path('view-product/',ProduitApi.as_view()),
    path('/update-product/<int:pk>',ProduitUpdateApi.as_view()),
    path('<int:pk>/delete',ProduitDeleteApi.as_view()),

    path('add-product-to-cart/',AddProductToCartAPI.as_view()),
    path('remove-product-from-cart/',RemoveProductToCartAPI.as_view()),

    path('create-order/',CreateOrderAPI.as_view()),

    path('add-product-to-wishlist/',AddProductToWishlistAPI.as_view()),
    path('create-wishlist/',CreateWishlistAPI.as_view()),



    
     

     
]