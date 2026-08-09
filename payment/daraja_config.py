from django_daraja.apps import DjangoDarajaConfig


class DarajaConfig(DjangoDarajaConfig):
    """Preserve django-daraja's historical AutoField migration contract."""

    default_auto_field = 'django.db.models.AutoField'
