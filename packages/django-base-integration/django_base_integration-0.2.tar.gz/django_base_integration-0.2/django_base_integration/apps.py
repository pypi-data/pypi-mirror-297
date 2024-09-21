"""Import modules for connecting signals and defining app config"""
from django.apps import AppConfig
from django.db.models.signals import pre_delete, pre_save


class IntegratorConfig(AppConfig):  # pylint: disable=function-redefined
    """
    App config
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_base_integration"
    label = "integrator"

    def ready(self) -> None:
        ...
