from django.conf import settings
from django.core.mail import send_mail

from .conf import authx_settings


def send_otp_email(to_email, code):
    subject = authx_settings.OTP_SUBJECT
    from_email = authx_settings.OTP_FROM_EMAIL or getattr(settings, "DEFAULT_FROM_EMAIL", None)

    message = (
        f"Your OTP code is {code}.\n\n"
        f"It will expire in {authx_settings.OTP_EXPIRY_MINUTES} minutes."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
    )