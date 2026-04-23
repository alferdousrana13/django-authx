## ⚡ Quick Setup

Get started in under 5 minutes:

### 1. Add apps

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework_simplejwt",
    "authx.apps.AuthxConfig",
]

#Configure user model
AUTH_USER_MODEL = "authx.User"

#Authentication backends
AUTHENTICATION_BACKENDS = [
    "authx.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]
#DRF + JWT setup
from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "authx.exceptions.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
#Add URLs
from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("authx.urls")),
]
#Run project
python manage.py migrate
python manage.py runserver

#Environment Configuration

Create a .env file in your project root:

cp .env.example .env
📧 Email Setup
Development (console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

OTP will be printed in the terminal.

Production (real email)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
AUTHX_OTP_FROM_EMAIL=your_email@gmail.com

⚠️ Use Gmail App Password (not normal password)

⚙️ Full Django Settings Example
from decouple import config, Csv
from datetime import timedelta

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

AUTH_USER_MODEL = "authx.User"

AUTHENTICATION_BACKENDS = [
    "authx.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "authx.exceptions.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

AUTHX_SETTINGS = {
    "OTP_LENGTH": config("AUTHX_OTP_LENGTH", default=6, cast=int),
    "OTP_EXPIRY_MINUTES": config("AUTHX_OTP_EXPIRY_MINUTES", default=10, cast=int),
    "OTP_SUBJECT": config("AUTHX_OTP_SUBJECT", default="Verify your email"),
    "OTP_FROM_EMAIL": config("AUTHX_OTP_FROM_EMAIL"),
    "LOGIN_REQUIRE_VERIFIED": config("AUTHX_LOGIN_REQUIRE_VERIFIED", default=True, cast=bool),
    "ALLOW_LOGIN": config("AUTHX_ALLOW_LOGIN", default=True, cast=bool),
}
🔌 API Endpoints
Method	Endpoint	Description
POST	/api/auth/signup/	Register user
POST	/api/auth/verify-otp/	Verify email
POST	/api/auth/resend-otp/	Resend OTP
POST	/api/auth/login/	Login
POST	/api/auth/token/refresh/	Refresh token
GET	/api/auth/me/	Current user
POST	/api/auth/forgot-password/	Send reset OTP
POST	/api/auth/reset-password/	Reset password
🔔 Signals
otp_created
user_verified
password_reset_done

Use for:

notifications
logging
analytics
onboarding
🧪 System Checks
python manage.py check

Validates:

missing user model
missing auth backend
missing DRF config
SMTP issues
📁 Environment Example

See .env.example file.

📦 PyPI

https://pypi.org/project/alfer-django-authx/

👤 Author

Al Ferdous