from rest_framework import generics
from rest_framework.response import Response
from .serializer import ClientSerializer
from .models import Clients



class ClientCreateApi(generics.CreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer



class ClientApi(generics.ListAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer

class ClientUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer


class ClientDeleteApi(generics.DestroyAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer