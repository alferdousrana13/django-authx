from django.dispatch import receiver

from .signals import otp_created, user_verified, password_reset_done


@receiver(otp_created)
def handle_otp_created(sender, user, otp, purpose, **kwargs):
    print(
        f"[AuthX Signal] OTP created for {user.email} | purpose={purpose} | code={otp.code}"
    )


@receiver(user_verified)
def handle_user_verified(sender, user, **kwargs):
    print(f"[AuthX Signal] User verified: {user.email}")


@receiver(password_reset_done)
def handle_password_reset_done(sender, user, **kwargs):
    print(f"[AuthX Signal] Password reset completed for: {user.email}")