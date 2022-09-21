from django.apps import AppConfig


class DjangoStarterAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_starter_app'


    def ready(self):
        # Register signals
        import django_starter_app.signals