from django.apps import AppConfig


class AuthxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authx"
    verbose_name = "AuthX"

    def ready(self):
        import authx.receivers
        import authx.checks