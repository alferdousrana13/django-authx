from django.dispatch import Signal

otp_created = Signal()
user_verified = Signal()
password_reset_done = Signal()