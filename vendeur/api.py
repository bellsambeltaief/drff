from rest_framework import generics
from rest_framework.response import Response
from .serializer import VendeurSerializer
from .models import Vendeur

class VendeurCreateApi(generics.CreateAPIView):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer

class VendeurApi(generics.ListAPIView):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer

class VendeurUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer

class VendeurDeleteApi(generics.DestroyAPIView):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer
