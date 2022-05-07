from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name","address")


class LoginSerializer(serializers.ModelSerializer):
    """
       serializer for login view
    """
    email = serializers.EmailField(max_length=255,min_length=8)
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=50,
        min_length=3,
        write_only=True
        )
    data = serializers.SerializerMethodField()

    def get_data(self,obj):
        user = User.objects.get(email=obj['email'])

        return {
            'token':user.get_jwt_token_for_user(),
            'id':user.id,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'address':user.address,

        }
    class Meta:
        model = User
        fields = ['email','password','data']
    
    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid email or password')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, check your email for activation')

        return {
            'email':user.email
        }
        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=50,
        min_length=5,
        write_only=True
        )
    class Meta:
        model = User
        fields = ('email','first_name','last_name','address', 'password','confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        user_data = validated_data
        user = User.objects.create_user(
                user_data.get('email'),
                user_data.get('password')
                
                )
        return user

class CustomEmailSerializerField(serializers.EmailField):
    def to_internal_value(self, value):
        value = super(CustomEmailSerializerField,
                      self).to_internal_value(value)
        return value.lower()

        
class SendOtpSerilizer(serializers.Serializer):
    email = CustomEmailSerializerField()


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    confirm_password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    otp_code = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'otp_code']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        otp_code = attrs.get('otp_code')

        if password != confirm_password:
            raise AuthenticationFailed('password did not match', 401)

        if UserOTP.objects.filter(otp=otp_code).exists():
            user_otp = UserOTP.objects.filter(otp=otp_code).first()
            user = user_otp.user

        if not UserOTP.objects.filter(otp=otp_code).exists():
            raise AuthenticationFailed('invalid otp', 401)


        user.set_password(password)
        user.save()

        return (user)

        return super().validate(attrs)
