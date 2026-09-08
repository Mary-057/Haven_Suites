from django.apps import AppConfig  # type: ignore[reportMissingModuleSource]


class GuestsSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guests_site'
