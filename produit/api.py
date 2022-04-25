from rest_framework import generics
from rest_framework.response import Response
from .serializer import ProduitSerializer
from .models import Produit



class ProduitCreateApi(generics.CreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitApi(generics.ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDeleteApi(generics.DestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer