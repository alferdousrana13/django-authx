from django.conf import settings
from django.core.checks import Error, Warning, register


@register()
def authx_settings_check(app_configs, **kwargs):
    errors = []

    # Check AUTH_USER_MODEL
    if getattr(settings, "AUTH_USER_MODEL", None) != "authx.User":
        errors.append(
            Warning(
                "AUTH_USER_MODEL is not set to 'authx.User'.",
                hint="Set AUTH_USER_MODEL = 'authx.User' if you are using the package user model.",
                id="authx.W001",
            )
        )

    # Check authentication backend
    backends = getattr(settings, "AUTHENTICATION_BACKENDS", [])
    if "authx.backends.EmailBackend" not in backends:
        errors.append(
            Warning(
                "authx.backends.EmailBackend is missing from AUTHENTICATION_BACKENDS.",
                hint="Add 'authx.backends.EmailBackend' to AUTHENTICATION_BACKENDS.",
                id="authx.W002",
            )
        )

    # Check DRF exception handler
    rest_framework = getattr(settings, "REST_FRAMEWORK", {})
    exception_handler = rest_framework.get("EXCEPTION_HANDLER")
    if exception_handler != "authx.exceptions.custom_exception_handler":
        errors.append(
            Warning(
                "Custom exception handler is not configured.",
                hint="Set REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'authx.exceptions.custom_exception_handler'.",
                id="authx.W003",
            )
        )

    # Check SMTP config if SMTP backend is used
    email_backend = getattr(settings, "EMAIL_BACKEND", "")
    if email_backend == "django.core.mail.backends.smtp.EmailBackend":
        if not getattr(settings, "EMAIL_HOST_USER", ""):
            errors.append(
                Error(
                    "EMAIL_HOST_USER is empty while using SMTP email backend.",
                    hint="Set EMAIL_HOST_USER in your environment or settings.",
                    id="authx.E001",
                )
            )
        if not getattr(settings, "EMAIL_HOST_PASSWORD", ""):
            errors.append(
                Error(
                    "EMAIL_HOST_PASSWORD is empty while using SMTP email backend.",
                    hint="Set EMAIL_HOST_PASSWORD in your environment or settings.",
                    id="authx.E002",
                )
            )

    return errors