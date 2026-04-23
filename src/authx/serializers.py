# authx/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .conf import authx_settings
from .email_utils import send_otp_email
from .models import EmailOTP
from .otp import create_email_otp
from .user_model import get_authx_user_model

User = get_authx_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp = create_email_otp(user)
        send_otp_email(user.email, otp.code)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "is_verified", "created_at"]


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        try:
            otp = EmailOTP.objects.filter(
                user=user,
                code=code,
                purpose=EmailOTP.Purpose.VERIFY,
                is_used=False,
            ).latest("created_at")
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid OTP."})

        if otp.is_expired():
            raise serializers.ValidationError({"code": "OTP has expired."})

        attrs["user"] = user
        attrs["otp"] = otp
        return attrs
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        try:
            otp = EmailOTP.objects.filter(
                user=user,
                code=code,
                purpose=EmailOTP.Purpose.RESET,
                is_used=False,
            ).latest("created_at")
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({"code": "Invalid reset OTP."})

        if otp.is_expired():
            raise serializers.ValidationError({"code": "OTP has expired."})

        attrs["user"] = user
        attrs["otp"] = otp
        return attrs
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")

        if authx_settings.LOGIN_REQUIRE_VERIFIED and not user.is_verified:
            raise serializers.ValidationError("Email is not verified")

        refresh = RefreshToken.for_user(user)

        return {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }