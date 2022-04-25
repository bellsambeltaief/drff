from django.urls import path
from .api import *
from django.views.decorators.csrf import csrf_exempt
from .views import ClientView


urlpatterns = [
    path('api',ClientApi.as_view()),
    path('api/create',ClientCreateApi.as_view()),
    path('api/<int:pk>',ClientUpdateApi.as_view()),
    path('api/<int:pk>/delete',ClientDeleteApi.as_view()),
    path('test/create', ClientView.as_view()),
    
   
]