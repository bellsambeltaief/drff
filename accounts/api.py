from rest_framework import status,generics,permissions
from rest_framework.response import Response 
from django.http import Http404
from accounts.serializers import *
from accounts.models import *
from django.conf import settings
from django.core.mail import send_mail




class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(serializer.data,status=status.HTTP_200_OK)

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.address = request.data['address']
        user.save()
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data})


class SendOtp(generics.CreateAPIView):
    """ endpoint to resend otp to user """
    permission_classes = (permissions.AllowAny,)
    serializer_class = SendOtpSerilizer


    def post(self, request, *args, **kwargs):
        """ resend the otp to user """
        email = request.data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
        user_otp = str(UserOTP.generate_account_otp(user,email=email))


        email_message      = 'Bonjour' +' ' +user.email + '\nVeuillez utiliser cet OTP code pour réinitialiser votre mot de passe  \n' +user_otp + '\n\nMerci d utiliser notre site!'


        from_email      = settings.DEFAULT_FROM_EMAIL
        to_email        = [user.email]
        email_subject   = 'Forgot password OTP'
        send_mail(
            email_subject,
            email_message,           
            from_email,
            to_email,
            fail_silently=False,
        )


        return Response(
            {'msg': "OTP sent successfully"},
            status=status.HTTP_200_OK)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
