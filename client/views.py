#from .models import Prod
#from .serializer import ProdSerializer
from rest_framework.generics import *
from .models import Clients
from rest_framework.views import APIView
from .serializer import ClientSerializer
from rest_framework.response import Response


#@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>',
        'Delete': '/task-delete/<str:pk>',

    }
    return Response(api_urls )

# Create your views here.

class ClientView(APIView):
    def post(self, request):
        serialize = ClientSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response({"msg": "created"})
        return Response({"msg": "error", "data": serialize.error_messages})
