import imp
from django.urls import path, include
from accounts.api import *

urlpatterns = [
    path('auth/login/',LoginAPIView.as_view(),name="login"),
    path('auth/register/', RegistrationAPI.as_view(),name="login"),
    path('auth/forgot-password/', SendOtp.as_view(),name="forgot-password"),
    path('auth/reset-password/', SetNewPasswordAPIView.as_view(),name="reset-password"),

    

]