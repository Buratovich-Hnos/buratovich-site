from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'website'

    # Connecting signals
    def ready(self):
        import website.signals
