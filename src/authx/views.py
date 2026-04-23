# authx/views.py
from rest_framework import permissions, status
from rest_framework.views import APIView
from .signals import user_verified, password_reset_done
from .user_model import get_authx_user_model

from .permissions import IsAdminRole
from .serializers import (
    SignupSerializer,
    UserSerializer,
    LoginSerializer,
    VerifyOTPSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .otp import create_email_otp
from .email_utils import send_otp_email
from .utils import success_response, error_response

User = get_authx_user_model()


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message="User created successfully. OTP sent to your email.",
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Login successful.",
            data=serializer.validated_data,
        )


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        was_unverified = not user.is_verified

        if was_unverified:
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            user_verified.send(sender=User, user=user)

        return success_response(
            message="Email verified successfully.",
            data={
                "email": user.email,
                "is_verified": user.is_verified,
            },
        )


class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return error_response(
                message="Email is required.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return error_response(
                message="User with this email does not exist.",
                status=status.HTTP_404_NOT_FOUND,
            )

        otp = create_email_otp(user)
        send_otp_email(user.email, otp.code)

        return success_response(
            message="OTP resent successfully.",
            data={"email": user.email},
        )


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        otp = create_email_otp(user, purpose="reset")
        send_otp_email(user.email, otp.code)

        return success_response(
            message="Password reset OTP sent to your email.",
            data={"email": user.email},
        )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save(update_fields=["password"])

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        password_reset_done.send(sender=User, user=user)

        return success_response(
            message="Password reset successful.",
            data={"email": user.email},
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return success_response(
            message="User profile fetched successfully.",
            data=serializer.data,
        )


class AdminOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request):
        return success_response(
            message="Welcome Admin!",
            data={
                "user": request.user.email,
                "role": request.user.role,
            },
        )