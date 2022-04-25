from django.urls import path, include
from .api import ProduitCreateApi , ProduitApi , ProduitUpdateApi , ProduitDeleteApi

urlpatterns = [
    path('api/create',ProduitCreateApi.as_view()),
     path('api/view',ProduitApi.as_view()),
     path('api/<int:pk>',ProduitUpdateApi.as_view()),
     path('api/<int:pk>/delete',ProduitDeleteApi.as_view()),
]