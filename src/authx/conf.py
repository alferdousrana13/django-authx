from django.conf import settings


DEFAULTS = {
    "OTP_LENGTH": 6,
    "OTP_EXPIRY_MINUTES": 5,
    "OTP_SUBJECT": "Your verification code",
    "OTP_FROM_EMAIL": None,
    "LOGIN_REQUIRE_VERIFIED": True,
    "ALLOW_LOGIN": True,
    "USE_PACKAGE_USER_MODEL": True,
}


class AuthXSettings:
    def __getattr__(self, attr):
        user_settings = getattr(settings, "AUTHX_SETTINGS", {})
        if attr in user_settings:
            return user_settings[attr]
        if attr in DEFAULTS:
            return DEFAULTS[attr]
        raise AttributeError(f"Invalid AuthX setting: '{attr}'")


authx_settings = AuthXSettings()