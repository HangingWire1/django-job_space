from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'  # This must match your app folder name

    def ready(self):
        # We import signals here so they are connected
        # as soon as the Django server starts.
        import authentication.signals