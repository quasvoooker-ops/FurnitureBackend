from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import OTP, UserProfile
from .serializers import *
from .utils import send_otp_email

class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        d = s.validated_data
        names = d['full_name'].split(' ', 1)
        user = User.objects.create_user(username=d['email'], email=d['email'], password=d['password'],
            first_name=names[0], last_name=names[1] if len(names)>1 else '', is_active=False)
        UserProfile.objects.create(user=user, role='customer', is_verified=False)
        send_otp_email(user, 'register')
        return Response({'detail': 'Check your email for the verification code.'}, status=201)

class VerifyOTPView(APIView):
    permission_classes = []
    def post(self, request):
        s = VerifyOTPSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        email, code, purpose = s.validated_data['email'].lower(), s.validated_data['code'], s.validated_data['purpose']
        try: user = User.objects.get(email=email)
        except User.DoesNotExist: return Response({'detail': 'User not found.'}, status=404)
        otp = OTP.objects.filter(user=user, code=code, purpose=purpose, is_used=False).order_by('-created_at').first()
        if not otp: return Response({'detail': 'Invalid OTP.'}, status=400)
        if otp.is_expired(): return Response({'detail': 'OTP expired. Request a new one.'}, status=400)
        otp.is_used = True; otp.save()
        if purpose == 'register':
            user.is_active = True; user.save()
            user.profile.is_verified = True; user.profile.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'role': user.profile.role, 'full_name': user.get_full_name(), 'email': user.email})

class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        s = LoginSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        user = authenticate(request, username=s.validated_data['email'].lower(), password=s.validated_data['password'])
        if not user: return Response({'detail': 'Invalid email or password.'}, status=401)
        if not user.is_active: return Response({'detail': 'Account not verified.'}, status=403)
        send_otp_email(user, 'login')
        return Response({'detail': 'OTP sent to your email.'})

class ResendOTPView(APIView):
    permission_classes = []
    def post(self, request):
        s = ResendOTPSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        try: user = User.objects.get(email=s.validated_data['email'].lower())
        except User.DoesNotExist: return Response({'detail': 'User not found.'}, status=404)
        send_otp_email(user, s.validated_data['purpose'])
        return Response({'detail': 'New OTP sent to your email.'})

class ForgotPasswordView(APIView):
    permission_classes = []
    def post(self, request):
        s = ForgotPasswordSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        try: user = User.objects.get(email=s.validated_data['email'].lower())
        except User.DoesNotExist: return Response({'detail': 'If that email exists, a code was sent.'})
        send_otp_email(user, 'reset')
        return Response({'detail': 'If that email exists, a code was sent.'})

class ResetPasswordView(APIView):
    permission_classes = []
    def post(self, request):
        s = ResetPasswordSerializer(data=request.data)
        if not s.is_valid(): return Response(s.errors, status=400)
        try: user = User.objects.get(email=s.validated_data['email'].lower())
        except User.DoesNotExist: return Response({'detail': 'User not found.'}, status=404)
        otp = OTP.objects.filter(user=user, code=s.validated_data['code'], purpose='reset', is_used=False).order_by('-created_at').first()
        if not otp: return Response({'detail': 'Invalid OTP.'}, status=400)
        if otp.is_expired(): return Response({'detail': 'OTP expired.'}, status=400)
        otp.is_used = True; otp.save()
        user.set_password(s.validated_data['new_password']); user.save()
        return Response({'detail': 'Password updated successfully.'})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out.'})

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserProfileSerializer(request.user.profile).data)
    