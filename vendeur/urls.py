from django.urls import path , include
from .api import VendeurCreateApi, VendeurApi, VendeurUpdateApi, VendeurDeleteApi


urlpatterns = [
    path('api/create',VendeurCreateApi.as_view()),
    path('api',VendeurApi.as_view()),
    path('api/<int:pk>',VendeurUpdateApi.as_view()),
    path('api/<int:pk>/delete',VendeurDeleteApi.as_view()),
]