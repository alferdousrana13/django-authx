from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .conf import authx_settings
from .models import EmailOTP
from .signals import otp_created


@transaction.atomic
def create_email_otp(user, purpose=EmailOTP.Purpose.VERIFY):
    EmailOTP.objects.filter(
        user=user,
        purpose=purpose,
        is_used=False,
    ).update(is_used=True)

    code = EmailOTP.generate_code(length=authx_settings.OTP_LENGTH)
    expires_at = timezone.now() + timedelta(minutes=authx_settings.OTP_EXPIRY_MINUTES)

    otp = EmailOTP.objects.create(
        user=user,
        code=code,
        purpose=purpose,
        expires_at=expires_at,
    )
    otp_created.send(
        sender=EmailOTP,
        user=user,
        otp=otp,
        purpose=purpose,
    )
    return otp