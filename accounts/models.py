from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser
from accounts.user_manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
import random


# Create your models here.
#testing

class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    password = models.CharField(max_length=400)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    # generate jwt token
    def get_jwt_token_for_user(self):
        """ get jwt token for the user """
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(days=7))
        return {            
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }
        


class UserOTP(models.Model):
    """ model for user otp"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "{0}-{1}".format(self.user, self.otp)

    def get_user(self):
        return self.user

    def get_otp(self):
        return self.otp

    def get_created_time(self):
        return self.created_on

    class Meta:
         verbose_name = "OTP Activiation"

    def generate_account_otp(self,email):
        otp_code = random.randint(111111, 999999)
        data = {
            'user': self,
            'otp': otp_code,
        }
        try:
            if UserOTP.objects.filter(user__email=email).exists():
                UserOTP.objects.filter(user__email=email).delete()
                user_otp = UserOTP.objects.create(**data)
            else:
                user_otp = UserOTP.objects.create(**data)
        except UserOTP.DoesNotExist:
            user_otp = UserOTP.objects.create(**data)
        return user_otp.otp



        