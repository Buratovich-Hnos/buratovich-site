from django.apps import AppConfig


class ExtranetConfig(AppConfig):
    name = 'extranet'

    # Connecting signals
    def ready(self):
        import extranet.signals