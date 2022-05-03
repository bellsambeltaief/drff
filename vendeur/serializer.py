from rest_framework import  serializers
from .models import Vendeur

class VendeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendeur
        fields = '__all__'